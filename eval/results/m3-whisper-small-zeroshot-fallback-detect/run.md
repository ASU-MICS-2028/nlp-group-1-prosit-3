---
title: "Whisper-small zero-shot, temperature fallback, language detected"
model: openai/whisper-small
owner: Joseph Etse
issue: "#6"
wer: "0.464"
gpu: Kaggle Tesla T4 (16 GB), free
cost: "0 USD"
date: 2026-11-24
ai-use: Claude ran it with the Kaggle command-line tool, downloaded the logs and wrote this record; Joseph reviews
---

# Whisper-small zero-shot, temperature fallback, language detected

- **Kaggle notebook:** private, `josephetse/m3-whisper-zeroshot-extra` version 1, code commit `7dc1099`, notebook `models/whisper_full/kaggle_zeroshot.ipynb`. Notebook-wide logs: `eval/results/m3-whisper-zeroshot-extra/`.
- **Command:** `zero_shot openai/whisper-small --fallback --detect`, then `common.score` (output in `stdout-predict-and-score.log`).
- **Model:** 244M parameters, no training. Same decoding as `m3-whisper-small-zeroshot-fallback`, except Whisper picks the language itself instead of being told English.
- **Time:** 4,032 s for the 1,000 clips (`predict.log`), much slower than the other runs because wrong-language clips loop and get re-decoded.
- **Result:** WER 0.464, CER 0.297; clinical 0.516, general 0.426 (`scores.json`), against 0.350 with English forced. 75 clips with WER > 1 (45 forced), 320 with spoken punctuation (347 forced) (`failure-checks.csv`).
- **What changed:** 469 of the 1,000 hypotheses differ from the forced-English run. 66 contain non-ASCII characters, for example Arabic-script, Bengali and Georgian text, so Whisper took accented English for another language.

See [[force-english-for-accented-speech]].
