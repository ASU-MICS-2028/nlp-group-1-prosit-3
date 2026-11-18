---
title: Instruction tuning (SFT) fine-tunes a pre-trained model on instruction-answer pairs so it follows requests
tags: [post-training, lecture-04]
source: knowledge/sources/lecture-04.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Instruction tuning (SFT) fine-tunes a pre-trained model on instruction-answer pairs so it follows requests

**Fine-tuning** means continuing to train an already-trained model on new data with the same next-token objective, because training from scratch costs a fortune. **Instruction tuning**, also called supervised fine-tuning (SFT), is fine-tuning where the data is (instruction, correct response) pairs. It is still next-token prediction: "nothing fancy is happening". It is the first step of post-training, after [[self-supervised-pretraining]].

Before SFT, a base model just continues text plausibly; Lecture 5's example: asked a question about shoplifting, it replies with another similar question. After SFT it answers. The aim is **generalisation** to new instructions, not memorisation of the training pairs.

**Example:** `Question: What is the capital of Ghana? Answer: Accra`, or "Translate 'hello friend' to French" with its answer.

**For Prosit 3:** fine-tuning Whisper on AfriSpeech (audio, transcript) pairs is the speech version of supervised fine-tuning.

Related: [[self-supervised-pretraining]], [[peft]], [[alignment-3h]], [[preference-data]]
