---
title: The Whisper fine-tuning loop is correct; check any training loop by overfitting one fixed batch
tags: [M3, whisper, training, debugging]
source: "issue #6; models/whisper_full/finetune.py"
author: Joseph Etse
ai-use: Claude wrote the loop and ran both checks; Joseph reviews
---

# The Whisper fine-tuning loop is correct; check any training loop by overfitting one fixed batch

**Question:** in the first smoke test (`whisper-tiny`, dev clips, learning rate 1e-4, a new batch every step), the loss went *up* from 0.86 to 2.21 over 40 steps. Is the loop broken?

**How we checked:** train repeatedly on one fixed batch of 8 clips at learning rate 1e-5. A correct loop must memorise it, so the loss falls towards 0. A loop with wrong labels cannot.

| Check | Loss at step 1 → 30 |
|---|---|
| One fixed batch, lr 1e-5 | 2.002 → 0.016 |
| New batch every step, lr 1e-4 (first smoke test) | 0.86 → 2.21 (rising) |

The labels decode to `<|en|><|transcribe|><|notimestamps|>The suppression of…`. The model adds the start token itself, so `pad_labels` drops it.

**Answer:** the loop is correct. The rise came from a learning rate 10 times our default, on a different batch every step. The real run uses 1e-5 with 500 warm-up steps.

**For M1, M2 and M4:** run this one-batch check before paying for GPU time. It takes about a minute on a laptop.

Related: [[whisper-zero-shot-loops-on-hard-clips]]
