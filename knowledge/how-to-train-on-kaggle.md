---
title: Train on Kaggle's free GPUs, with every run's logs saved as proof
tags: [gpu, kaggle, how-to]
source: "issue #6; decision 0012; models/whisper_full/kaggle_finetune.ipynb"
author: Joseph Etse
ai-use: Claude wrote the steps and the notebook; Joseph checks them on the first run
---

# Train on Kaggle's free GPUs, with every run's logs saved as proof

Kaggle gives each verified account **30 GPU hours a week** for free. Sessions last up to **12 hours** and keep running after you close the browser if you use "Save & Run All". Decision 0012 says why we use Kaggle.

## One-time setup (each person, about 10 minutes)

1. Create an account at kaggle.com. A personal email is fine.
2. **Verify your phone number:** Settings → Phone verification. Without it, the GPU and Internet options stay greyed out.
3. Create a notebook: **Code → New Notebook → File → Import Notebook**, then upload `models/whisper_full/kaggle_finetune.ipynb` from the repo.
4. In the right panel, **Session options**:
   - Accelerator: **GPU T4 x2**. Not the P100: recent PyTorch no longer supports it.
   - Internet: **On**.
   - Persistence: Files only (optional).

No tokens or keys are needed, because both the repo and the dataset mirror are public. Never paste a key into a Kaggle notebook. Notebooks can be made public by mistake.

## Start a run

1. Optional: check the first cells interactively. Run cells 1 to 3 and check that:
   - `nvidia-smi` shows a T4;
   - `cuda True` is printed;
   - `df` shows at least about 45 GB free. If not, lower `--train-files` in cell 4. Each file is about 2 GB and about 2,000 clips.
2. **Save Version → Save & Run All (Commit) → Save.** This runs the whole notebook in the background, even with the browser closed. It is the only mode that survives closing the tab.
3. Watch it from **Your Work → the notebook → Versions → the running version → Logs**.

## What gets saved (the proof)

When the version finishes, its **Output** tab holds:

| Path | What it is | Commit it? |
|---|---|---|
| `m3-whisper-small-afrispeech/train.log` | every line the training printed, across all sessions | yes |
| `m3-whisper-small-afrispeech/train_log.csv` | step, loss, learning rate, time, dev WER: for the loss curve in the report | yes |
| `m3-whisper-small-afrispeech/environment-session-*.json` | git commit, GPU, library versions, the exact settings, one per session | yes |
| `m3-whisper-small-afrispeech/stdout-*.log`, `machine-*.log` | raw output including warnings and errors; `nvidia-smi` and disk space | yes |
| `m3-whisper-small-afrispeech/predictions.csv`, `predict.log`, `scores.json` | the test-set result, after training finishes | yes |
| `checkpoints/whisper-small-afrispeech/best/`, `last/` | model weights, about 1 GB and 3 GB | **never** |

Download the `m3-…` folder into `eval/results/` and commit it with a `run.md`. Add a row to `docs/gpu-log.md` with Kaggle T4, the hours (from `train.log`) and 0 USD. Also link the Kaggle version URL in `run.md` as extra proof.

## If the run stops before 4,000 steps

The script saves its state every 500 steps and stops cleanly after `--max-hours 10`, so the session's 12 h limit never cuts it off mid-save.

To continue:
1. Open the notebook, then **Add Input → Your Work → Notebooks**, and pick this notebook's previous version.
2. **Save & Run All** again.

Cell 3 copies the previous logs and the `last/` state in, and training continues from the saved step. Resumed sessions see a new data shuffle, and `train.log` says so.

## Things that can go wrong

- **`cuda False` in cell 2:** the accelerator is off, or the phone is not verified.
- **Out of memory:** lower `--batch` to 4 and raise `--accumulate` to 4. The effective batch stays at 16.
- **Disk full while downloading:** lower `--train-files`.
- **Quota:** check the hours left at the top of the notebook editor. One full run is about 6–10 h of the 30 per week.

Related: [[how-to-score-a-model]], [[save-every-result-to-a-file]], [[environment]]
