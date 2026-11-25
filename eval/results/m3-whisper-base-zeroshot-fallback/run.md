---
title: "Whisper-base zero-shot, temperature fallback"
model: openai/whisper-base
owner: Joseph Etse
issue: "#6"
wer: "0.464"
gpu: Kaggle Tesla T4 (16 GB), free
cost: "0 USD"
date: 2026-11-24
ai-use: Claude ran it with the Kaggle command-line tool, downloaded the logs and wrote this record; Joseph reviews
---

# Whisper-base zero-shot, temperature fallback

- **Kaggle notebook:** private, `josephetse/m3-whisper-zeroshot-extra` version 1, code commit `7dc1099`, notebook `models/whisper_full/kaggle_zeroshot.ipynb`. Notebook-wide logs: `eval/results/m3-whisper-zeroshot-extra/`.
- **Command:** `zero_shot openai/whisper-base --fallback`, then `common.score` (output in `stdout-predict-and-score.log`).
- **Model:** 74M parameters, no training. Forced English, same decoding as the whisper-small zero-shot run.
- **Time:** 533 s for the 1,000 clips (`predict.log`).
- **Result:** WER 0.464, CER 0.268; clinical 0.520, general 0.423 (`scores.json`). 77 clips with WER > 1, 254 with spoken punctuation not in the reference (`failure-checks.csv`).

See [[bigger-whisper-helps-zero-shot]].
