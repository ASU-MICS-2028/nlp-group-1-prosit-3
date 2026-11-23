"""M3: Whisper as it is (no training) on the shared test set.

    uv run python -m models.whisper_full.zero_shot openai/whisper-small [--fallback]
    uv run python -m models.whisper_full.zero_shot checkpoints/<name>/best --fallback   # a fine-tuned model

--fallback re-decodes with rising temperature when the output is too repetitive (gzip compression
ratio above 1.35) or too unlikely, Whisper's own defence against loops like "i do i do i do".

Writes predictions.csv, predict.log and an environment file to eval/results/m3-<model>-zeroshot[-fallback]/,
or for a fine-tuned checkpoint to eval/results/m3-<name>/ next to its training logs. Then score with common.score.
"""

import csv
import sys
import time
from pathlib import Path

import torch
from transformers import pipeline

from common.data import fetch_test_audio, load_audio, load_test_set
from common.runlog import RunLog, environment, save_json


def run_dir(name: str, fallback: bool) -> Path:
    """Hub models get a zero-shot folder; a local checkpoints/<name>/best goes to eval/results/m3-<name>."""
    path = Path(name)
    if path.is_dir():
        return Path("eval/results") / f"m3-{path.parent.name if path.name == 'best' else path.name}"
    return Path("eval/results") / (f"m3-{name.split('/')[-1]}-zeroshot" + ("-fallback" if fallback else ""))


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    name = args[0] if args else "openai/whisper-small"
    fallback = "--fallback" in sys.argv
    gen = {"language": "en", "task": "transcribe"}
    if fallback:
        gen |= {"temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0), "compression_ratio_threshold": 1.35, "logprob_threshold": -1.0}
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    asr = pipeline("automatic-speech-recognition", model=name, device=device,
                   chunk_length_s=30)  # 13 test clips are longer than Whisper's 30 s window
    out = run_dir(name, fallback)
    log = RunLog(out / "predict.log")
    env = environment() | {"model": name, "generate_kwargs": {k: str(v) for k, v in gen.items()}}
    save_json(out / "environment-predict.json", env)
    log(f"=== predicting with {name} on {env['device']}, commit {env['git_commit'][:7]}, fallback={fallback}")

    paths = fetch_test_audio()
    rows = load_test_set()
    start = time.time()
    with open(out / "predictions.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["audio_id", "hypothesis"])
        for i, row in enumerate(rows, 1):
            text = asr(load_audio(paths[row["audio_id"]]), generate_kwargs=gen)["text"]
            w.writerow([row["audio_id"], text.strip()])
            if i % 50 == 0:
                log(f"{i}/{len(rows)}  {time.time() - start:.0f}s")
    log(f"=== done in {time.time() - start:.0f}s on {device}: {out / 'predictions.csv'}")


if __name__ == "__main__":
    main()
