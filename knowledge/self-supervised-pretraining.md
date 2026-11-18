---
title: Pre-training hides part of unlabelled text and learns to predict it, so no human labels are needed
tags: [training, lecture-01]
source: knowledge/sources/lecture-01.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Pre-training hides part of unlabelled text and learns to predict it, so no human labels are needed

Labelled data is scarce, but raw text is everywhere. **Self-supervised pre-training** turns raw text into training examples: hide a word (or the next word) and train the model to predict it. The hidden word acts as a **pseudo-label**, so no human labelling is needed and models can train at internet scale.

GPT means **Generative Pre-trained Transformer**. OpenAI scaled transformers on web data and performance kept rising (the "scaling laws" result), but bigger models also need more data. Pre-training is the expensive first stage; adapting the model afterwards is post-training (see [[instruction-tuning]]).

**Example (Lecture 5):** from "I am going to school", the model sees "I am going to" and must predict "school". The text itself supplies the answer.

**For Prosit 3:** Whisper was pre-trained on far more speech than AfriSpeech's 200 hours. That head start is the main argument for a pre-trained transformer over an RNN trained from scratch on Ayamra's data.

Related: [[instruction-tuning]], [[data-size-decides-which-model-wins]], [[lm-outputs-a-distribution]]
