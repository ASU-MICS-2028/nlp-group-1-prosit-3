---
title: Fine-tuning whisper-small on the Mac crashed and restarted it, so training runs go to Kaggle
tags: [M3, whisper, gpu]
source: "issue #6; decision 0012"
author: Joseph Etse
ai-use: Claude started the test without asking and wrote this note; Joseph reported the crash
---

# Fine-tuning whisper-small on the Mac crashed and restarted it, so training runs go to Kaggle

**Question:** can we measure whisper-small's training speed on the laptop (Apple M3, 24 GB shared memory) to estimate GPU cost?

**Options compared and how:** one attempt, 20 steps at batch 16 on dev clips (`finetune --model openai/whisper-small --train-split dev --steps 20 --batch 16 --eval-clips 0`).

| Option | Result |
|---|---|
| whisper-tiny on the Mac, batch 4 (earlier smoke test) | ran fine, about a minute |
| whisper-small on the Mac, batch 16 | **the laptop crashed and restarted**, and no log survived |

**Winner and why:** none on the laptop. A batch of 16 thirty-second clips through a 244M-parameter model, with its gradients and the optimiser's copies, needs more memory than the Mac can share safely with everything else running. Training goes to Kaggle (decision 0012). The cost estimate came from published speeds instead.

**Limits:**
- We did not find the largest batch the Mac can handle, and we won't try again.
- Zero-shot prediction (no training) ran fine on the Mac for both whisper-small and turbo.

Related: [[check-a-training-loop-by-overfitting-one-batch]], [[how-to-train-on-kaggle]]
