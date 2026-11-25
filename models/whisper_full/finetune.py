"""M3: fine-tune all of Whisper's weights on AfriSpeech-200.

    # smoke test on the laptop: tiny model, a few dev clips, loss should go down
    uv run python -m models.whisper_full.finetune --model openai/whisper-tiny --train-split dev --steps 30 --eval-clips 0
    # the real run, on Kaggle (see knowledge/how-to-train-on-kaggle.md)
    uv run python -m models.whisper_full.finetune --model openai/whisper-small --steps 4000 --batch 8 --accumulate 2 --max-hours 10

Trains on --train-split, checks WER on --eval-clips dev clips every --eval-every steps.
Proof of the run (committed): eval/results/m3-<name>/ holds train.log (every printed line),
train_log.csv (one row per logged step) and environment.json (git commit, GPU, versions, settings).
Weights (never committed): checkpoints/<name>/best is the best dev WER, checkpoints/<name>/last is the
state to resume from. Running the same command again resumes from last; --max-hours stops cleanly
before a time-limited session (Kaggle: 12 h) is killed. Predict with:
    uv run python -m models.whisper_full.zero_shot checkpoints/<name>/best --fallback
"""

import argparse
import csv
import io
import os
import random
import time
from pathlib import Path

import jiwer
import librosa
import pyarrow.parquet as pq
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor

from common.data import split_files
from common.runlog import RunLog, environment, save_json
from common.score import normalize

MAX_SECONDS = 30  # Whisper hears 30 s at most; longer training clips would be cut mid-sentence
MAX_LABEL_TOKENS = 448  # Whisper's decoder length


def pad_labels(labels: list[list[int]], start_token: int | None = None) -> torch.Tensor:
    """Pad token lists with -100, which the loss ignores. The model adds the start token itself, so drop it."""
    if start_token is not None:
        labels = [l[1:] if l and l[0] == start_token else l for l in labels]
    width = max(len(l) for l in labels)
    return torch.tensor([l + [-100] * (width - len(l)) for l in labels])


def save_state(path: Path, model, opt, sched, scaler, step: int, best: float) -> None:
    """Everything needed to carry on after a disconnect. Written to a temporary file first, so a kill mid-save
    leaves the previous state intact."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    state = {"model": model.state_dict(), "opt": opt.state_dict(), "sched": sched.state_dict(),
             "scaler": scaler.state_dict(), "step": step, "best": best}
    torch.save(state, path / "trainer.pt.tmp")
    os.replace(path / "trainer.pt.tmp", path / "trainer.pt")


def load_state(path: Path, model, opt, sched, scaler) -> tuple[int, float]:
    """Restore a saved state into the given objects; returns (step, best dev WER), or (0, inf) when there is none."""
    file = Path(path) / "trainer.pt"
    if not file.exists():
        return 0, float("inf")
    state = torch.load(file, map_location="cpu", weights_only=False)
    model.load_state_dict(state["model"])
    opt.load_state_dict(state["opt"])
    sched.load_state_dict(state["sched"])
    scaler.load_state_dict(state["scaler"])
    return state["step"], state["best"]


def clips(split: str, seed: int, limit: int | None = None):
    """Yield (audio, transcript) forever, in shuffled order, reading one Parquet chunk at a time (train is 55 GB)."""
    rng = random.Random(seed)
    files = split_files(split, limit)
    while True:
        rng.shuffle(files)
        for f in files:
            batch = []
            for part in pq.ParquetFile(f).iter_batches(batch_size=64, columns=["audio", "transcript", "duration"]):
                batch += [r for r in part.to_pylist() if r["duration"] <= MAX_SECONDS and r["transcript"].strip()]
            rng.shuffle(batch)
            for r in batch:
                audio, _ = librosa.load(io.BytesIO(r["audio"]["bytes"]), sr=16000, mono=True)
                yield audio, " ".join(r["transcript"].split())


def make_batch(items, processor, device):
    audio, text = zip(*items)
    features = processor.feature_extractor(list(audio), sampling_rate=16000, return_tensors="pt").input_features
    labels = [l[:MAX_LABEL_TOKENS] for l in processor.tokenizer(list(text)).input_ids]
    sot = processor.tokenizer.convert_tokens_to_ids("<|startoftranscript|>")
    return features.to(device), pad_labels(labels, start_token=sot).to(device)


def dev_wer(model, processor, device, n: int) -> float:
    model.eval()
    refs, hyps = [], []
    data = clips("dev", seed=0)  # same dev clips every time, so the numbers compare
    with torch.no_grad():
        for _ in range(n):
            audio, text = next(data)
            feats = processor.feature_extractor(audio, sampling_rate=16000, return_tensors="pt").input_features.to(device)
            ids = model.generate(feats, language="en", task="transcribe", max_new_tokens=MAX_LABEL_TOKENS - 8)
            refs.append(normalize(text))
            hyps.append(normalize(processor.batch_decode(ids, skip_special_tokens=True)[0]))
    model.train()
    return jiwer.wer(refs, hyps)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="openai/whisper-small")
    ap.add_argument("--train-split", default="train")
    ap.add_argument("--train-files", type=int, default=None, help="use only the first N parquet files (disk limit)")
    ap.add_argument("--steps", type=int, default=4000)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--accumulate", type=int, default=1, help="gradient accumulation: effective batch = batch x accumulate")
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--warmup", type=int, default=500)
    ap.add_argument("--eval-every", type=int, default=500)
    ap.add_argument("--eval-clips", type=int, default=200)
    ap.add_argument("--max-hours", type=float, default=None, help="save and stop after this long (resume later)")
    ap.add_argument("--name", default=None)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    name = args.name or f"{args.model.split('/')[-1]}-afrispeech"
    results = Path("eval/results") / f"m3-{name}"
    log = RunLog(results / "train.log")
    best_dir, last_dir = Path("checkpoints") / name / "best", Path("checkpoints") / name / "last"

    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    processor = WhisperProcessor.from_pretrained(args.model, language="en", task="transcribe")
    model = WhisperForConditionalGeneration.from_pretrained(args.model).to(device)
    model.generation_config.forced_decoder_ids = None  # language and task are passed to generate() instead

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr)
    warm = max(1, args.warmup)
    sched = torch.optim.lr_scheduler.LambdaLR(  # linear warm-up, then linear decay to 0
        opt, lambda s: min((s + 1) / warm, max(0.0, (args.steps - s) / max(1, args.steps - warm))))
    use_amp = device == "cuda"
    scaler = torch.amp.GradScaler(enabled=use_amp)
    done, best = load_state(last_dir, model, opt, sched, scaler)

    env = environment() | {"command_args": vars(args), "resumed_from_step": done}
    save_json(results / f"environment-session-{env['started'].replace(':', '')}.json", env)
    log(f"=== session start {env['started']} on {env['device']}, commit {env['git_commit'][:7]}, "
        + (f"resuming from step {done} (best dev WER {best:.3f})" if done else "fresh start"))
    log(f"settings: {vars(args)}")
    torch.manual_seed(args.seed + done)
    data = clips(args.train_split, args.seed + done, args.train_files)  # a resumed session sees a new shuffle

    new_csv = not (results / "train_log.csv").exists()
    table = open(results / "train_log.csv", "a", newline="", encoding="utf-8")
    rows = csv.writer(table)
    if new_csv:
        rows.writerow(["step", "loss", "lr", "session_seconds", "dev_wer"])

    model.train()
    start = time.time()
    step = done
    for step in range(done + 1, args.steps + 1):
        for _ in range(args.accumulate):
            feats, labels = make_batch([next(data) for _ in range(args.batch)], processor, device)
            with torch.autocast(device_type="cuda", dtype=torch.float16, enabled=use_amp):
                loss = model(input_features=feats, labels=labels).loss / args.accumulate
            scaler.scale(loss).backward()
        scaler.unscale_(opt)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(opt)
        scaler.update()
        opt.zero_grad()
        sched.step()
        wer = ""
        if args.eval_clips and (step % args.eval_every == 0 or step == args.steps):
            wer = dev_wer(model, processor, device, args.eval_clips)
            log(f"step {step}  dev WER {wer:.3f} on {args.eval_clips} clips")
            if wer < best:
                best = wer
                model.save_pretrained(best_dir)
                processor.save_pretrained(best_dir)
                log(f"  saved best to {best_dir}")
        if step % 10 == 0 or wer != "":
            lr = sched.get_last_lr()[0]
            log(f"step {step}  loss {loss.item() * args.accumulate:.3f}  lr {lr:.2e}  {time.time() - start:.0f}s")
            rows.writerow([step, f"{loss.item() * args.accumulate:.4f}", f"{lr:.3e}", f"{time.time() - start:.0f}",
                           f"{wer:.4f}" if wer != "" else ""])
            table.flush()
        if step % args.eval_every == 0:
            save_state(last_dir, model, opt, sched, scaler, step, best)
        if args.max_hours and time.time() - start > args.max_hours * 3600:
            save_state(last_dir, model, opt, sched, scaler, step, best)
            log(f"=== stopped at step {step} after {args.max_hours} h; run the same command again to resume")
            table.close()
            return
    table.close()
    save_state(last_dir, model, opt, sched, scaler, step, best)
    if not args.eval_clips:
        model.save_pretrained(best_dir)
        processor.save_pretrained(best_dir)
    log(f"=== done: step {step}, {time.time() - start:.0f}s this session; best dev WER {best:.3f}; checkpoint {best_dir}")


if __name__ == "__main__":
    main()
