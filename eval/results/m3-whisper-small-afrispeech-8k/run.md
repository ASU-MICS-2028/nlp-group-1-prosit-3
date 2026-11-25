---
title: "Whisper-small fully fine-tuned on AfriSpeech-200 (8,000 steps, Kaggle T4)"
model: openai/whisper-small, all weights fine-tuned
owner: Joseph Etse
issue: "#6"
wer: "0.152"
gpu: Kaggle Tesla T4 (16 GB), free
cost: "0 USD"
date: 2026-11-25
ai-use: Claude started the run with the Kaggle command-line tool, downloaded the logs and wrote this record; Joseph approved the run and reviews
---

# Whisper-small fully fine-tuned on AfriSpeech-200 (8,000 steps, Kaggle T4)

- **Kaggle notebook:** private, `josephetse/m3-whisper-small-afrispeech-8k` version 1. Pushed at 20:18 UTC on 2026-11-24; the session ran from about 20:19 to 01:54 UTC on 2026-11-25 (20,073 s, about 5.6 GPU hours, `kaggle-notebook-log.json`).
- **Code:** commit `810230a` on `6-whisper`, notebook `models/whisper_full/kaggle_finetune.ipynb`.
- **Command:** as the 4,000-step run (`eval/results/m3-whisper-small-afrispeech/run.md`) with `--name whisper-small-afrispeech-8k --steps 8000`. Started from the released weights, not from the 4k checkpoint, so the learning-rate decay spans all 8,000 steps.
- **Time:** training 18,977 s (about 2.37 s per step); prediction of 1,000 clips 918 s.
- **Dev WER** (200 clips, every 500 steps, `train.log`): 0.169 at step 4,000, 0.160 at 5,000, best **0.150 at 7,500**, 0.154 at 8,000. The step-7,500 checkpoint was used for the test set.

## Results on the 1,000-clip test set

| Model | WER | CER | Clinical | General | Hausa | Igbo | Swahili | Yoruba | Zulu | WER > 1 | Spoken punct. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| fine-tuned, 4,000 steps | 0.156 | 0.071 | 0.200 | 0.123 | 0.145 | 0.158 | 0.111 | 0.161 | 0.135 | 10 | 12 |
| **fine-tuned, 8,000 steps** | **0.152** | **0.070** | **0.194** | **0.121** | 0.145 | 0.154 | 0.105 | 0.141 | 0.126 | 11 | 9 |

From `scores.json` and `failure-checks.csv`. See [[training-longer-gains-little]].
