---
title: "M3: Whisper zero-shot + full fine-tune"
owner: Joseph Etse
issue: "#6"
status: doing (fine-tune done: WER 0.156; report and slides next)
ai-use: Claude drafted the plan and the zero-shot script; Joseph reviews
---

# Plan for #6: Whisper zero-shot + full fine-tune

## Goal

Measure how well Whisper transcribes AfriSpeech **with no training** (zero-shot), then fine-tune all its weights on the train split and measure again on the same 1,000 test clips. Zero-shot predictions go out early so M5 can start the demo and the error analysis.

## Steps

1. Zero-shot `whisper-small` on the test set, on the Mac (MPS). Save in `eval/results/m3-whisper-small-zeroshot/`.
2. Zero-shot one larger model (`whisper-large-v3-turbo`) if it runs at a sane speed, so we know how much size alone buys.
3. Write the fine-tuning script and test it on a few hundred dev clips locally (a few steps only, checking that the loss goes down).
4. Full fine-tune `whisper-small` on Kaggle (`models/whisper_full/kaggle_finetune.ipynb`, steps in `knowledge/how-to-train-on-kaggle.md`), on the train split, choosing checkpoints on dev.
5. Score, write the learnings, draft the Section B subsection and the slide segment.

## Alternatives to compare

- Model size: tiny / base / small / large-v3-turbo, zero-shot. Same test set, same scorer.
- Forcing English (`language="en"`) versus letting Whisper detect the language. Accented English is sometimes misdetected as another language.
- Fine-tuning: all weights (this issue) versus LoRA (M4, Eric). Same base model so the comparison is fair.

## Failure cases

- Clips longer than 30 s (13 of 1,000, up to 138 s): Whisper only hears 30 s, so the pipeline chunks them.
- Hallucination: Whisper invents or repeats text on silence or noise. Look for hypotheses much longer than the reference.
- Out of memory on the GPU during fine-tuning: lower the batch size, use gradient accumulation and fp16.
- Medical terms and drug doses ("lasix 220mg"): expected to be the main errors, checked in the error analysis.

## GPU cost estimate

Zero-shot: none (Mac). Full fine-tune of `whisper-small`: Kaggle's free T4 (decision 0012), about 4 GPU hours of the 30-hour weekly quota (measured in the Kaggle trial), 0 USD. Batch 8 × accumulate 2, all 28 train files. On a rented L4, A10 or A100 it would be 2–5 hours and 2–5 USD.

## Done when

- `eval/results/<run>/predictions.csv` and `run.md` exist for every run reported, and `scores.json` was produced by `uv run python -m common.score`
- Learnings written in `learnings/`, one finding per file, including the options that lost
- Section B subsection drafted and the slide segment added
- Every GPU run logged in `docs/gpu-log.md`, with `train.log`, `train_log.csv` and the environment files committed as proof
- Change file in `docs/changes/` and PR merged
