---
title: Parameter-efficient fine-tuning trains only a small subset of parameters instead of the whole model
tags: [post-training, lecture-05]
source: knowledge/sources/lecture-05.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Parameter-efficient fine-tuning trains only a small subset of parameters instead of the whole model

Retraining every weight of a huge base model needs enormous compute and data, because every gradient step touches every weight ([[backprop-and-gradient-descent]]). **PEFT** (parameter-efficient fine-tuning) trains only a small set of parameters and still works well. LoRA is one specific PEFT technique ([[lora]]).

**Example (Lecture 5 setup):** input x = [3, 4, 9] (1×3) times W (3×2, 6 parameters) gives h = xW (1×2). Full fine-tuning updates all 6. PEFT freezes W and trains something smaller alongside it; at real scale that is thousands of parameters instead of millions.

**For Prosit 3:** the course reading Ghimire et al. 2024 uses PEFT for low-resource ASR. Fine-tuning Whisper with LoRA on AfriSpeech is the cheap middle ground between using Whisper as is and full fine-tuning.

Related: [[lora]], [[instruction-tuning]], [[backprop-and-gradient-descent]]
