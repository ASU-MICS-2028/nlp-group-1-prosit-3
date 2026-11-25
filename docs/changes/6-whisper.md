---
title: "M3: Whisper zero-shot (four sizes) and full fine-tune of whisper-small on Kaggle"
owner: Joseph Etse
issue: "#6"
pr: "#TBD"
ai-use: "Claude Code wrote the code, notebooks and tests, ran every run through the Kaggle CLI and drafted the records and the Section B draft; Joseph directed the work, set up Kaggle, reviewed the draft and checked the numbers against the run files"
---

# M3: Whisper zero-shot and full fine-tune

## What changed

- **Zero-shot Whisper** (`models/whisper_full/zero_shot.py`): predicts the 1,000-clip test set with any Whisper model or fine-tuned checkpoint. It has options for temperature fallback (`--fallback`) and for letting Whisper detect the language (`--detect`).
- **Full fine-tuning** (`models/whisper_full/finetune.py`): trains every weight of a Whisper model on AfriSpeech-200 train, with:
  - checkpoints chosen by WER on dev clips;
  - resume after interruption;
  - `--max-hours` to stop cleanly before a session ends.
- **Kaggle notebooks:** `models/whisper_full/kaggle_finetune.ipynb` (train, predict, score) and `kaggle_zeroshot.ipynb` (several zero-shot runs). Setup and the command-line method are in `knowledge/how-to-train-on-kaggle.md`.
- **Proof for every run** (`common/runlog.py`): every log line goes to a file, and the code version, hardware and libraries are recorded. `common/data.py` can limit the number of train files.
- **Failure checks** (`models/whisper_full/failure_checks.py`): counts repetition loops (clips with WER > 1) and dictated punctuation written as words.
- **Results** (9 runs, all on the same 1,000 test clips):

  | Run | WER |
  |---|---|
  | tiny, zero-shot | 0.571 |
  | base, zero-shot | 0.464 |
  | small, zero-shot | 0.350 |
  | small, zero-shot, language detected | 0.464 |
  | large-v3-turbo, zero-shot | 0.293 |
  | **small, fine-tuned, 4k steps** | **0.156** |
  | small, fine-tuned, 8k steps | 0.152 |

  Small zero-shot without fallback reached 0.480. A 20-step Kaggle trial checked the pipeline.
- **Report:** the Section B subsection and slide segment are in `report/drafts/m3-whisper.md`.
- 36 tests.

## AI use in detail

- **What AI did (Claude Code):**
  - wrote all the code, notebooks and tests listed above;
  - pushed and watched every Kaggle run through the Kaggle command-line tool, then downloaded the logs and checked them for secrets;
  - wrote the run records (`run.md`), the learnings and the GPU log rows;
  - drafted the Section B subsection and the slide segment, and proposed the nurse analogy;
  - ran one unrequested speed test on Joseph's laptop, which crashed it (see `learnings/dont-fine-tune-on-the-laptop.md`). Since then, heavy jobs run only on Kaggle and only with Joseph's approval.
- **What Joseph did himself:**
  - directed the work: chose to train on Kaggle's free GPUs (decision 0012), approved each run including the optional ones (tiny, base, language detection, 8k steps), and chose the 4k model as the headline result;
  - set the rule that every run is logged to files as proof;
  - created the Kaggle account and API token and connected the command-line tool;
  - read and edited the Section B and slide draft, and chose the nurse analogy for the whole deck (decision 0013).
- **How Joseph checked the AI's part:** read the draft and the run records, and checked the reported numbers against the run files (`scores.json`, logs). He did not read all the code line by line. The code is covered by the 36 tests, and by the runs themselves, whose logs are committed.

## Produced

- Learnings:
  - `learnings/bigger-whisper-helps-zero-shot.md`
  - `learnings/whisper-zero-shot-loops-on-hard-clips.md`
  - `learnings/whisper-writes-spoken-punctuation-as-words.md`
  - `learnings/force-english-for-accented-speech.md`
  - `learnings/fine-tuning-whisper-small-halves-wer.md`
  - `learnings/training-longer-gains-little.md`
  - `learnings/check-a-training-loop-by-overfitting-one-batch.md`
  - `learnings/some-references-contain-text-nobody-said.md`
  - `learnings/dont-fine-tune-on-the-laptop.md`
- Decisions:
  - `docs/decisions/0012-kaggle-free-gpus.md` (Accepted)
  - `docs/decisions/0013-deck-analogy-nurse-learning-the-ward.md` (Proposed; waiting for the team)
- Results:
  - `eval/results/m3-whisper-small-zeroshot/`
  - `eval/results/m3-whisper-small-zeroshot-fallback/`
  - `eval/results/m3-whisper-large-v3-turbo-zeroshot-fallback/`
  - `eval/results/m3-whisper-tiny-zeroshot-fallback/`
  - `eval/results/m3-whisper-base-zeroshot-fallback/`
  - `eval/results/m3-whisper-small-zeroshot-fallback-detect/`
  - `eval/results/m3-whisper-small-afrispeech/`
  - `eval/results/m3-whisper-small-afrispeech-8k/`
  - `eval/results/m3-kaggle-smoke/`
  - notebook logs in `eval/results/m3-whisper-zeroshot-extra/`
- GPU: 4 Kaggle runs, 10.2 GPU hours, 0 USD (`docs/gpu-log.md`).
