---
title: Cross-entropy loss measures the gap between the predicted distribution and the one-hot truth
tags: [training, lecture-03-part-2]
source: knowledge/sources/lecture-03-part-2.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Cross-entropy loss measures the gap between the predicted distribution and the one-hot truth

The ground truth for one prediction is a **one-hot** distribution: 1 on the correct token and 0 on everything else. Cross-entropy measures how far the model's predicted distribution is from that. Because the truth is one-hot, it reduces to **loss = −log(p_correct)**, the negative log of the probability given to the right token. As that probability rises, the loss falls.

**Worked numbers (Lecture 3, natural log):** the correct token "to" gets 0.01, so loss = −ln 0.01 ≈ 4.6. Training pushes it to 0.1 (loss ≈ 2.3), then 0.2 (≈ 1.6). At probability 1 the loss would be 0.

The training step: the forward pass makes the prediction, cross-entropy scores it, and [[backprop-and-gradient-descent]] adjusts the weights.

**For Prosit 3:** Whisper is fine-tuned with cross-entropy on its output tokens; an RNN with CTC uses a different loss built on the same −log probability idea ([[ctc]]).

Related: [[lm-outputs-a-distribution]], [[backprop-and-gradient-descent]], [[perplexity]], [[ctc]]
