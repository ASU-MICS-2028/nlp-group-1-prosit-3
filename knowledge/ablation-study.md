---
title: An ablation study removes parts one at a time to see what each contributed
tags: [experiments, lecture-04]
source: knowledge/sources/lecture-04.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# An ablation study removes parts one at a time to see what each contributed

No theory tells you in advance which technique will help, so NLP is experimental. When several changes together improve a result, an **ablation study** removes them one at a time (and in combinations) and measures again, so you know which change actually mattered. It also follows **no free lunch**: a gain in one direction usually costs something in another, and ablations show what each gain cost.

**Example (Lecture 4):** add techniques A, B and C and the score rises from 80% to 90%. Remove A only: still 90%, so A did nothing and can go. Remove B only: 82%, so B carried most of the gain.

**For Prosit 3:** if Whisper + LoRA + data augmentation beats the RNN, we should check which part did the work, for example Whisper with and without augmentation, all scored with [[word-error-rate]] on the same test set.

Related: [[measure-before-adding-complexity]], [[parameters-vs-hyperparameters]], [[word-error-rate]]
