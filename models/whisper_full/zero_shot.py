"""M3: Whisper as it is (no training) on the shared test set.

    uv run python -m models.whisper_full.zero_shot openai/whisper-small [--fallback]

--fallback re-decodes with rising temperature when the output is too repetitive (gzip compression
ratio above 1.35) or too unlikely, Whisper's own defence against loops like "i do i do i do".

Writes eval/results/m3-<model>-zeroshot/predictions.csv, then score it with common.score.
"""

import csv
import sys
import time
from pathlib import Path

import torch
from transformers import pipeline

from common.data import fetch_test_audio, load_audio, load_test_set


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
    out = Path("eval/results") / (f"m3-{name.split('/')[-1]}-zeroshot" + ("-fallback" if fallback else ""))
    out.mkdir(parents=True, exist_ok=True)

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
                print(f"{i}/{len(rows)}  {time.time() - start:.0f}s", flush=True)
    print(f"done in {time.time() - start:.0f}s on {device}: {out / 'predictions.csv'}")


if __name__ == "__main__":
    main()
