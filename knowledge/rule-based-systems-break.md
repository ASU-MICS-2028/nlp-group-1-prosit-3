---
title: Rule-based NLP breaks because every new rule meets a case it gets wrong
tags: [history, lecture-01]
source: knowledge/sources/lecture-01.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Rule-based NLP breaks because every new rule meets a case it gets wrong

Before machine learning, NLP systems used hand-written rules. ELIZA, the early chatbot, looked clever but only matched patterns. Rule-based translation swapped words using a dictionary (a *lexicon*) and produced broken output.

The problem is coverage: language has endless variations, and each new rule meets a sentence that breaks it. Machine learning flips the approach: you write a learning algorithm, give it many labelled examples (a **corpus**), and it finds the patterns itself.

**Example (Lecture 1):** the class wrote `check_sentiment(sentence)`, which looks for words from a negative list (hate, not, sad) and a positive list (love, like, enjoy). It calls "I don't hate jollof" negative, because it sees "hate" and "not", even though the sentence is positive. Mixed sentences also fail.

**For Prosit 3:** nobody could write rules mapping every African accent's sounds to letters, which is why ASR is learned from data such as [[afrispeech-200]].

Related: [[neuron-weighted-sum]], [[self-supervised-pretraining]]
