---
title: Preference data asks people to pick the better of two outputs, which is easier than writing good ones
tags: [alignment, lecture-06]
source: knowledge/sources/lecture-06.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Preference data asks people to pick the better of two outputs, which is easier than writing good ones

Writing a perfect example answer is hard. Choosing which of two answers is better is easy. **Preference data** collects those choices; ChatGPT showing two answers or two images and asking which you prefer is collecting it. The choices are often used to train a **scoring (reward) model**, which then guides further training with [[reinforcement-learning]]. That pipeline is what RLHF (reinforcement learning from human feedback) means (source: lecture-06.md; Jurafsky and Martin).

**Example:** a user sees two replies to "explain malaria simply" and clicks the clearer one. Thousands of such clicks train a model to score clarity.

**For Prosit 3:** doctors correcting transcripts produce something similar: a preferred (corrected) version versus the model's version, useful for later fine-tuning.

Related: [[reinforcement-learning]], [[alignment-3h]], [[human-in-the-loop]]
