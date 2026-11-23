"""M3: fine-tune all of Whisper's weights on AfriSpeech-200.

    # smoke test on the laptop: tiny model, a few dev clips, loss should go down
    uv run python -m models.whisper_full.finetune --model openai/whisper-tiny --train-split dev --steps 30 --eval-clips 0
    # the real run, on the shared GPU
    uv run python -m models.whisper_full.finetune --model openai/whisper-small --steps 4000

Trains on --train-split, checks WER on --eval-clips dev clips every --eval-every steps, and keeps the
best checkpoint in checkpoints/<name>/ (never committed). Predict with:
    uv run python -m models.whisper_full.zero_shot checkpoints/<name> --fallback
"""

import argparse
import io
import random
import time
from pathlib import Path

import jiwer
import librosa
import pyarrow.parquet as pq
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor

from common.data import split_files
from common.score import normalize

MAX_SECONDS = 30  # Whisper hears 30 s at most; longer training clips would be cut mid-sentence
MAX_LABEL_TOKENS = 448  # Whisper's decoder length


def pad_labels(labels: list[list[int]], start_token: int | None = None) -> torch.Tensor:
    """Pad token lists with -100, which the loss ignores. The model adds the start token itself, so drop it."""
    if start_token is not None:
        labels = [l[1:] if l and l[0] == start_token else l for l in labels]
    width = max(len(l) for l in labels)
    return torch.tensor([l + [-100] * (width - len(l)) for l in labels])


def clips(split: str, seed: int):
    """Yield (audio, transcript) forever, in shuffled order, reading one Parquet chunk at a time (train is 55 GB)."""
    rng = random.Random(seed)
    files = split_files(split)
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
    ap.add_argument("--steps", type=int, default=4000)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--accumulate", type=int, default=1, help="gradient accumulation: effective batch = batch x accumulate")
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--warmup", type=int, default=500)
    ap.add_argument("--eval-every", type=int, default=500)
    ap.add_argument("--eval-clips", type=int, default=200)
    ap.add_argument("--name", default=None)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    processor = WhisperProcessor.from_pretrained(args.model, language="en", task="transcribe")
    model = WhisperForConditionalGeneration.from_pretrained(args.model).to(device)
    model.generation_config.forced_decoder_ids = None  # language and task are passed to generate() instead
    out = Path("checkpoints") / (args.name or f"{args.model.split('/')[-1]}-afrispeech")

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr)
    warm = max(1, args.warmup)
    sched = torch.optim.lr_scheduler.LambdaLR(  # linear warm-up, then linear decay to 0
        opt, lambda s: min((s + 1) / warm, max(0.0, (args.steps - s) / max(1, args.steps - warm))))
    use_amp = device == "cuda"
    scaler = torch.amp.GradScaler(enabled=use_amp)
    data = clips(args.train_split, args.seed)

    best = float("inf")
    model.train()
    start = time.time()
    for step in range(1, args.steps + 1):
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
        if step % 10 == 0:
            print(f"step {step}  loss {loss.item() * args.accumulate:.3f}  lr {sched.get_last_lr()[0]:.2e}  {time.time() - start:.0f}s", flush=True)
        if args.eval_clips and (step % args.eval_every == 0 or step == args.steps):
            wer = dev_wer(model, processor, device, args.eval_clips)
            print(f"step {step}  dev WER {wer:.3f} on {args.eval_clips} clips", flush=True)
            if wer < best:
                best = wer
                model.save_pretrained(out)
                processor.save_pretrained(out)
                print(f"  saved best to {out}", flush=True)
    if not args.eval_clips:
        model.save_pretrained(out)
        processor.save_pretrained(out)
    print(f"done in {time.time() - start:.0f}s; best dev WER {best:.3f}; checkpoint {out}")


if __name__ == "__main__":
    main()
