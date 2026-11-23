---
title: "Whisper-small zero-shot, temperature fallback"
model: openai/whisper-small
owner: Joseph Etse
issue: "#6"
wer: "0.350"
gpu: Apple M3 (mps), local
cost: "0 USD"
date: 2026-11-23
ai-use: Claude wrote the script and ran it; Joseph reviews
---

# Whisper-small zero-shot, temperature fallback

- **Command:** `uv run python -m models.whisper_full.zero_shot openai/whisper-small --fallback`, then `uv run python -m common.score eval/results/m3-whisper-small-zeroshot-fallback/predictions.csv`
- **Model:** `openai/whisper-small` (244M parameters), no training
- **Decoding:** temperature fallback (0.0 to 1.0 in steps of 0.2, compression ratio threshold 1.35, logprob threshold -1.0), forced English, 30 s chunks for the 13 longer clips
- **Libraries:** transformers and torch 5.24.0 2.15.0
- **Time:** 1869 s for the 1,000 clips (2.8 hours of audio) on an Apple M3 laptop
- **Result:** overall WER 0.350. All numbers are in `scores.json`.

See [[whisper-zero-shot-loops-on-hard-clips]] and [[whisper-writes-spoken-punctuation-as-words]].
