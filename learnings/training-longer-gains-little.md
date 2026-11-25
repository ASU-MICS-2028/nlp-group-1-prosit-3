---
title: Doubling fine-tuning from 4,000 to 8,000 steps gains only 0.4 WER points
tags: [M3, whisper, fine-tuning]
source: "issue #6; eval/results/m3-whisper-small-afrispeech/, eval/results/m3-whisper-small-afrispeech-8k/"
author: Joseph Etse
ai-use: Claude ran both fine-tunes on Kaggle and wrote the note; Joseph reviews
---

# Doubling fine-tuning from 4,000 to 8,000 steps gains only 0.4 WER points

**Question:** dev WER was still falling at step 4,000. Does training twice as long help?

**Options compared and how:** whisper-small fully fine-tuned with identical settings except the number of steps, each from the released weights; best dev checkpoint scored on the same 1,000 test clips.

| Steps | GPU time | Best dev WER | Test WER | Clinical | General |
|---|---|---|---|---|---|
| 4,000 | 2.8 h | 0.161 | 0.156 | 0.200 | 0.123 |
| 8,000 | 5.6 h | 0.150 | **0.152** | 0.194 | 0.121 |

**Winner and why:** 8,000 steps is slightly better everywhere, but the gain (0.4 points) is small for double the GPU time, and it may be within run-to-run noise. Most of what fine-tuning buys arrives in the first 4,000 steps.

**Limits:** one seed per setting; dev WER uses 200 clips, so differences under about 1 point are not reliable.

Related: [[fine-tuning-whisper-small-halves-wer]]
