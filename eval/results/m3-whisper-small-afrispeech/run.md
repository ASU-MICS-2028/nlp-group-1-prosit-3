---
title: "Whisper-small fully fine-tuned on AfriSpeech-200 (4,000 steps, Kaggle T4)"
model: openai/whisper-small, all weights fine-tuned
owner: Joseph Etse
issue: "#6"
wer: "0.156"
gpu: Kaggle Tesla T4 (16 GB), free
cost: "0 USD"
date: 2026-11-24
ai-use: Claude wrote the training script and notebook, started the run with the Kaggle command-line tool, downloaded the logs and wrote this record; Joseph approved the run and reviews
---

# Whisper-small fully fine-tuned on AfriSpeech-200 (4,000 steps, Kaggle T4)

- **Kaggle notebook:** private, `josephetse/m3-whisper-small-afrispeech` version 1.
  - Pushed at 10:05 UTC on 2026-11-24 and **queued for about 4 hours**.
  - The session ran from 14:07 to about 16:57 UTC.
- **Code:** commit `bded701` on `6-whisper`, notebook `models/whisper_full/kaggle_finetune.ipynb`.
- **Command** (from cell 0): `finetune --name whisper-small-afrispeech --model openai/whisper-small --steps 4000 --batch 8 --accumulate 2 --max-hours 10`. Then `zero_shot checkpoints/whisper-small-afrispeech/best --fallback` and `common.score`.
- **Training settings:**
  - Data: all 28 train files (about 57,800 clips; clips longer than 30 s and empty transcripts skipped).
  - Effective batch 16.
  - AdamW, learning rate 1e-5 with 500 warm-up steps, then a linear decay to 0.
  - fp16 mixed precision and gradient clipping at 1.0.
  - The best checkpoint was chosen by WER on the same 200 dev clips, checked every 500 steps.
- **Machine and libraries** (`machine-*.log`, `environment-*.json`): Tesla T4 15 GB, Python 3.13.16, torch 2.15.0+cu132, transformers 5.24.0.
- **Time:**
  - Training: 9,015 s, about 2.5 h, so about 2.25 s per step.
  - Prediction of 1,000 clips: 878 s.
  - Whole session: about 2.8 GPU hours.

## Results on the 1,000-clip test set

| Model | WER | CER | Clinical | General | Hausa | Igbo | Swahili | Yoruba | Zulu |
|---|---|---|---|---|---|---|---|---|---|
| whisper-small zero-shot (fallback) | 0.350 | 0.204 | 0.389 | 0.322 | 0.315 | 0.404 | 0.269 | 0.345 | 0.307 |
| whisper-large-v3-turbo zero-shot (fallback) | 0.293 | 0.174 | 0.345 | 0.255 | 0.278 | 0.293 | 0.238 | 0.288 | 0.256 |
| **whisper-small fine-tuned (fallback)** | **0.156** | **0.071** | **0.200** | **0.123** | 0.145 | 0.158 | 0.111 | 0.161 | 0.135 |

All numbers come from `scores.json` and the zero-shot runs' `scores.json`.

## Training curve (dev WER on 200 clips, from `train.log`)

| Step | 500 | 1000 | 1500 | 2000 | 2500 | 3000 | 3500 | 4000 |
|---|---|---|---|---|---|---|---|---|
| Dev WER | 0.212 | 0.199 | 0.192 | 0.182 | 0.174 | 0.167 | 0.164 | 0.161 |

Dev WER was still falling at step 4,000, slowly, so more steps might help a little. The loss for every 10th step is in `train_log.csv`.

## Did fine-tuning fix the zero-shot failures? (`failure-checks.csv`)

Produced by `uv run python -m models.whisper_full.failure_checks` on all three predictions files.

| Model | Clips with WER above 1 (loops) | Clips with spoken punctuation not in the reference |
|---|---|---|
| small zero-shot | 45 | 347 |
| turbo zero-shot | 35 | 383 |
| **small fine-tuned** | **10** | **12** |

The punctuation counts use a slightly wider word list than the earlier learning, so they don't match its 335 exactly.

## Proof files in this folder

| File | What it holds |
|---|---|
| `train.log` | every line the training script printed |
| `train_log.csv` | loss and learning rate every 10 steps, and dev WER every 500 |
| `stdout-train-*.log`, `stdout-predict.log`, `stdout-score.log` | raw output, including warnings |
| `kaggle-notebook-log.json` | Kaggle's own log of the notebook |
| `environment-*.json` | the code commit, GPU, library versions and exact settings |
| `predictions.csv`, `predict.log`, `scores.json` | the test predictions and their scores |

The weights (`best/` and `last/`) stay in the Kaggle notebook's output and are never committed.

**Warnings in the logs:** the same harmless ones explained in `eval/results/m3-kaggle-smoke/run.md`.

See [[fine-tuning-whisper-small-halves-wer]].
