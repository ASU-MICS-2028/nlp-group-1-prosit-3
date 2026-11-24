---
title: Fully fine-tuning whisper-small on AfriSpeech cuts WER from 0.350 to 0.156, beating the 3× larger turbo zero-shot
tags: [M3, whisper, fine-tuning]
source: "issue #6; eval/results/m3-whisper-small-afrispeech/, eval/results/m3-whisper-small-zeroshot-fallback/, eval/results/m3-whisper-large-v3-turbo-zeroshot-fallback/"
author: Joseph Etse
ai-use: Claude ran the training on Kaggle, scored it and wrote the note; Joseph reviews
---

# Fully fine-tuning whisper-small on AfriSpeech cuts WER from 0.350 to 0.156, beating the 3× larger turbo zero-shot

**Question:** how much does training on AfriSpeech buy, compared with using Whisper as it is, or with using a bigger Whisper?

**Options compared and how:**
- the same 1,000 test clips, the same scorer, and temperature fallback for all three;
- the fine-tune trained 4,000 steps at an effective batch of 16 on the train split, on a free Kaggle T4, in about 2.8 GPU hours.

| Option | WER | Clinical | General | Loops (WER > 1) | Spoken punctuation |
|---|---|---|---|---|---|
| whisper-small zero-shot, 244M parameters | 0.350 | 0.389 | 0.322 | 45 | 347 |
| whisper-large-v3-turbo zero-shot, 809M | 0.293 | 0.345 | 0.255 | 35 | 383 |
| **whisper-small fine-tuned** | **0.156** | **0.200** | **0.123** | **10** | **12** |

**Winner and why:** the fine-tuned small model. It makes less than half the word errors of the zero-shot small model, and about half those of a model three times its size. Training taught it our transcription style: it writes "comma" and "full stop" as words in 12 clips instead of over 300. It also learned the accents and the medical vocabulary, and it loops far less. Every accent improved: Swahili is now 0.111 and Yoruba 0.161.

**Limits:**
- Clinical speech is still the hardest at 0.200 vs 0.123. The error analysis (M5) should show which medical words it still misses.
- Dev WER was still falling at step 4,000 (0.164 → 0.161), so a longer run might gain a little more.
- This is one run with one seed.
- It does not show whether LoRA (M4) gets close at lower cost. That's Eric's comparison.

Related: [[bigger-whisper-helps-zero-shot]], [[whisper-zero-shot-loops-on-hard-clips]], [[whisper-writes-spoken-punctuation-as-words]], [[how-to-train-on-kaggle]]
