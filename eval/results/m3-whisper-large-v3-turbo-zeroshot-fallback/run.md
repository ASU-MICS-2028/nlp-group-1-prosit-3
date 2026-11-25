---
title: "Whisper-large-v3-turbo zero-shot, temperature fallback"
model: openai/whisper-large-v3-turbo
owner: Joseph Etse
issue: "#6"
wer: "0.293"
gpu: Apple M3 (mps), local
cost: "0 USD"
date: 2026-11-23
ai-use: Claude ran the script and wrote this record; Joseph reviews
---

# Whisper-large-v3-turbo zero-shot, temperature fallback

- **Command:** `uv run python -m models.whisper_full.zero_shot openai/whisper-large-v3-turbo --fallback`, then `uv run python -m common.score eval/results/m3-whisper-large-v3-turbo-zeroshot-fallback/predictions.csv`
- **Model:** `openai/whisper-large-v3-turbo` (809M parameters: the large-v3 encoder with a 4-layer decoder), no training
- **Decoding:** temperature fallback (0.0 to 1.0 in steps of 0.2, compression ratio threshold 1.35, logprob threshold -1.0), forced English, 30 s chunks
- **Libraries:** transformers and torch 5.24.0 2.15.0
- **Time:** 1878 s for the 1,000 clips on an Apple M3 laptop, while a smoke test shared the GPU
- **Result:** overall WER 0.293 (clinical 0.345, general 0.255). All numbers are in `scores.json`.

See [[bigger-whisper-helps-zero-shot]].
