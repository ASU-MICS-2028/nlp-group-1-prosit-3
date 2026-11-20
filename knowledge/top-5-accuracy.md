---
title: Top-5 accuracy is the share of examples whose true label is among the model's five most likely predictions
tags: [evaluation, lecture-09]
source: knowledge/sources/lecture-09.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Top-5 accuracy is the share of examples whose true label is among the model's five most likely predictions

Normal (top-1) accuracy counts a prediction as right only if the model's single most likely label is correct. **Top-5 accuracy** counts it right if the true label is anywhere in the model's five most likely labels. It suits tasks with many similar classes. Lecture 9 flagged not knowing this as a mistake, and stressed defining metrics exactly. Do not confuse it with top-k *sampling* ([[decoding-strategies]]).

**Worked number:** on 100 images, the true label is ranked first 60 times and ranked 2nd to 5th another 25 times. Top-1 accuracy is 60%; top-5 accuracy is 85%.

**For Prosit 3:** the same care applies to our metrics: define [[word-error-rate]] exactly (substitutions + deletions + insertions over reference words), including how we normalise case and punctuation.

Related: [[decoding-strategies]], [[word-error-rate]]
