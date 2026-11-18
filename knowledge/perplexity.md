---
title: Perplexity measures how surprised a language model is by real text; lower is better
tags: [evaluation, lecture-02]
source: knowledge/sources/lecture-02.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Perplexity measures how surprised a language model is by real text; lower is better

Lecture 2 said to judge a language model first by reading its output, "later with perplexity", without defining it. The standard definition (source: lecture-02.md; Jurafsky and Martin, ch. 3): perplexity is the inverse probability the model gives a test text, normalised by the number of words, **PP = P(w_1 ... w_N)^(-1/N)**. Equivalently, 2 to the power of the average cross-entropy per word.

Intuition: it is the effective number of words the model is choosing between at each step. Lower perplexity means the model finds real text less surprising, so it models the language better. It must be computed on held-out text with the same tokenizer, or numbers are not comparable.

**Worked number:** if a model gives every word of a 4-word test sentence probability 0.1, then P = 0.1^4 and PP = (0.1^4)^(-1/4) = 10, as if picking among 10 equally likely words.

**For Prosit 3:** our main metric is [[word-error-rate]], not perplexity, because a speech model's output is judged against a reference transcript.

Related: [[n-gram-language-model]], [[cross-entropy-loss]], [[word-error-rate]], [[byte-pair-encoding]]
