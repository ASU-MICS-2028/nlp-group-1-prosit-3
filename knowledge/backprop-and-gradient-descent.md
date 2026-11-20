---
title: Backpropagation computes the gradients; gradient descent uses them to update every weight
tags: [training, lecture-03-part-2]
source: knowledge/sources/lecture-03-part-2.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Backpropagation computes the gradients; gradient descent uses them to update every weight

Two separate steps that people often blur:
- **Backpropagation** is the algorithm that computes the gradient of the loss with respect to every weight (how much the loss changes if that weight moves).
- **Gradient descent** updates the weights by stepping against the gradient: **W_new = W − learning rate × gradient**. (Lecture 6 wrote "+", meaning a step in the direction that lowers the loss; check your textbook's sign convention.)

All weights are updated, including the encoder's, because the error may start there. Lecture 3's analogy: failing a quiz on React may really be a gap in JavaScript. The gradient has the same shape as W, so with billions of weights each step is costly, which motivates [[lora]].

**Worked number:** a weight of 0.50 with gradient 2.0 and learning rate 0.01 becomes 0.50 − 0.02 = 0.48.

**For Prosit 3:** full fine-tuning of Whisper updates every weight this way; LoRA updates only small added matrices.

Related: [[cross-entropy-loss]], [[parameters-vs-hyperparameters]], [[lora]], [[peft]]
