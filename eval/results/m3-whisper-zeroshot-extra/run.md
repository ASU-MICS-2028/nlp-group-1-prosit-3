---
title: "Kaggle notebook: extra zero-shot runs (tiny, base, small with language detection)"
owner: Joseph Etse
issue: "#6"
gpu: Kaggle Tesla T4 (16 GB), free
cost: "0 USD"
date: 2026-11-24
ai-use: Claude pushed the notebook with the Kaggle command-line tool, downloaded the logs and wrote this record; Joseph approved the run and reviews
---

# Kaggle notebook: extra zero-shot runs

- **Notebook:** private, `josephetse/m3-whisper-zeroshot-extra` version 1, pushed 20:18 UTC on 2026-11-24, code commit `7dc1099`.
- **Session:** about 20:29 to 21:56 UTC, 5,220 s (about 1.45 GPU hours, `m3-whisper-zeroshot-extra.log`).
- **Machine:** `machine-*.log` (nvidia-smi and disk). Libraries in each run's `environment-predict.json`.
- **Downloaded** with `kaggle kernels output ... --file-pattern '^(m3-|[^/]*\.log$)'`; checked for tokens before committing (none).
- **Runs:**
  - `eval/results/m3-whisper-tiny-zeroshot-fallback/`: WER 0.571
  - `eval/results/m3-whisper-base-zeroshot-fallback/`: WER 0.464
  - `eval/results/m3-whisper-small-zeroshot-fallback-detect/`: WER 0.464
