---
title: LoRA fine-tunes a big model by training two small matrices instead of the full weights
tags: [fine-tuning, M4]
source: knowledge/sources/lecture-06.md; knowledge/sources/prosit-1.md
author: Joseph Etse
ai-use: Claude drafted from the source; Joseph reviewed
---

# LoRA fine-tunes a big model by training two small matrices instead of the full weights

Freeze a weight matrix **W** (K×D) and learn a low-rank update **A** (K×R) × **B** (R×D). The forward pass becomes **h = xW + xAB**, and only A and B are trained.

**Worked example (Lecture 6):** for W of 300×200 there are 60,000 weights. At rank R = 3, A has 900 and B has 600, so **1,500 are trained instead of 60,000**. At the break-even rank R = KD/(K+D) = 120, LoRA saves nothing.

- **Why it works:** a small part of the weights drives most task behaviour. Training finds which ones; you don't pick them.
- **Adapters can be swapped:** keep one frozen base model plus small adapters per task or domain.
- **We used it before:** Prosit 1 fine-tuned Qwen2.5-0.5B and SmolLM2-135M with LoRA, DoRA and full fine-tuning on health and agriculture text ([[prosit-1]]).
- **For Ayamra (M4):** if Whisper + LoRA gets close to full fine-tuning's WER at a fraction of the GPU cost and storage, that is a strong practical argument for a hospital network.

Related: [[encoder-decoder]], [[word-error-rate]]
