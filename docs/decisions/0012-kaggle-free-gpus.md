---
title: Train on Kaggle's free T4 GPUs, with logs saved as proof
status: Accepted
date: 2026-11-23
decided-by: Joseph
ai-use: Claude compared the options and estimated costs; Joseph chose Kaggle
---

# 0012. Train on Kaggle's free T4 GPUs, with logs saved as proof

## Context

Fine-tuning needs a GPU. Decision 0005 left the paid provider and spending ceiling open. The estimate for fine-tuning whisper-small (4,000 steps × 16 clips, about 180 hours of audio) was:
- 2–5 USD on a rented L4, A10 or A100;
- 10–25 USD for the whole team.

We would rather spend nothing. Training on a laptop is not an option: it crashed the Mac (see learnings).

## Options considered

- **Rented GPU (RunPod, Vast and similar):** fastest at about 2–5 hours, but it costs money and needs a shared key.
- **Google Colab free:** a T4, but the session ends when the browser is idle for about 90 minutes, and the quota is not published.
- **Kaggle Notebooks:** a T4 with 30 GPU hours a week per account. 12-hour sessions keep running with the browser closed ("Save & Run All"). The output is kept with each notebook version.

## Decision

Use Kaggle (GPU T4 x2) for the M3 full fine-tune, and offer it to M1, M2 and M4.

How we run it:
- `finetune.py` saves its state every 500 steps and stops after `--max-hours`, so a run can span sessions.
- It writes `train.log`, `train_log.csv` and an environment file per session into `eval/results/<run>/`. Those files, plus the Kaggle version URL, are the proof that gets committed.
- whisper-small uses batch 8 × accumulate 2 (effective batch 16) on 16 GB.
- It uses all 28 train files. The trial run showed 2.5 TB of free disk on `/`, so the 14-file limit planned at first is not needed.

## Consequences

- Costs 0 USD. Each `docs/gpu-log.md` row still records the hours.
- About 4 hours per whisper-small run, measured at about 2.5 s per step in the trial (`eval/results/m3-kaggle-smoke/`). A rented GPU would take 2–5 hours.
- A full fine-tune of `whisper-large-v3-turbo` does not fit in 16 GB. It would need a rented GPU under 0005.
