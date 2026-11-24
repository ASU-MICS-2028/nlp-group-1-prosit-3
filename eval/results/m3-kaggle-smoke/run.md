---
title: "Kaggle trial run: 20 training steps, then predict and score the test set"
model: openai/whisper-small (20 steps, effectively untrained)
owner: Joseph Etse
issue: "#6"
wer: "0.341 (not a fine-tuning result)"
gpu: Kaggle Tesla T4 (16 GB), free
cost: "0 USD"
date: 2026-11-24
ai-use: Claude built the trial notebook, started it with the Kaggle command-line tool and wrote this record; Joseph set up the account and approved the trial
---

# Kaggle trial run: 20 training steps, then predict and score the test set

**Purpose:** check the whole Kaggle pipeline before spending 10 GPU hours on it: setup, data download, training, saving checkpoints, prediction, scoring and logs. It is **not** a result for the report. With 20 steps the learning rate is still near 0 (warm-up is 500 steps), so the model is essentially zero-shot whisper-small.

- **Kaggle notebook:** private, `josephetse/m3-kaggle-smoke` version 1. Started with `kaggle kernels push --accelerator NvidiaTeslaT4` on 2026-11-24 at 00:47 UTC; finished at about 01:08 UTC.
- **Code:** commit `ca0ef7a` on branch `6-whisper`. Notebook `models/whisper_full/kaggle_finetune.ipynb`, with cell 0 set to `RUN = "kaggle-smoke"` and `TRAIN_ARGS = "--model openai/whisper-small --steps 20 --batch 8 --accumulate 2 --train-files 1 --eval-every 10 --eval-clips 10"`.
- **Machine** (`machine-*.log`): 2 × Tesla T4 15 GB (one used), driver 580, CUDA 13.0. Disk: `/kaggle/working` 20 GB, and `/` 2.5 TB free.
- **Libraries** (`environment-*.json`): Python 3.13.16 (picked by uv), torch 2.15.0+cu132, transformers 5.24.0.

## What the logs show

| Stage | Result | Proof |
|---|---|---|
| Training, 20 steps at batch 8 × 2 | about **2.5 s per step**: 97 s for 20 steps, including 2 dev checks of 10 clips | `train.log`, `train_log.csv`, `stdout-train-*.log` |
| Best checkpoint and resume state saved | yes: `best/` and `last/` (3.6 GB together, not committed) | `train.log` |
| Prediction, 1,000 test clips with fallback | 974 s on the T4 | `predict.log`, `stdout-predict.log` |
| Scoring | WER 0.341 (clinical 0.385, general 0.308) | `scores.json`, `stdout-score.log` |
| Whole Kaggle session | about 21 minutes | `kaggle-notebook-log.json` (Kaggle's own log of the notebook) |

The WER is close to zero-shot whisper-small on the Mac (0.350). The model barely moved in 20 steps, so the small gap is not evidence of anything.

## Harmless warnings in the logs

- `Error in sitecustomize … No module named 'wrapt'`: Kaggle's own start-up file fails to import in our uv environment. It changes nothing.
- `lr_scheduler.step() before optimizer.step()`: with fp16, the first step is skipped when the gradient scale is being calibrated. This is normal.
- `unauthenticated requests to the HF Hub`: the mirror is public. A token would only raise download rate limits.
- `chunk_length_s is very experimental`: the same 30 s chunking as in the Mac zero-shot runs, so the results stay comparable.

## What changes for the real run

1. **Disk is not a limit.** `/` has 2.5 TB free, so the real run uses all 28 train files (about 57,800 clips) instead of 14.
2. **Faster than estimated.** At about 2.5 s per step, 4,000 steps take about 3 hours, plus about 25 minutes of dev checks, plus about 16 minutes for prediction. That's roughly 4 hours in all, against the 6–10 estimated. The `--max-hours 10` stop stays as a safety net.
