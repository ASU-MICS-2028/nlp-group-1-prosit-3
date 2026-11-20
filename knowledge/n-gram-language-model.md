---
title: An n-gram model predicts the next word from only the previous N-1 words
tags: [language-models, lecture-02]
source: knowledge/sources/lecture-02.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# An n-gram model predicts the next word from only the previous N-1 words

An n-gram model is a Markov chain over words: the next word depends only on the last N-1 words. A bigram looks at one word back, a trigram at two, a 4-gram at three. Bigger N gives more fluent text but needs more data, because longer word sequences are seen less often. "Language model" is the umbrella term; n-grams are the non-neural kind and LLMs are one neural kind.

- **Start of a sentence:** a beginning-of-sentence token `<s>` is added in training, so the model learns what usually comes first.
- **Grammar checking:** "they is dancing" is rare in a corpus compared with "they are dancing", so it gets very low probability and can be flagged.
- With n-grams, say "context", not "attention"; attention is a neural-network term.

**Example (Lecture 2, blocks in a bucket):** a bigram can produce "I live TV", because it only sees "live" when choosing the next word. A trigram sees "I live" and is more likely to pick "in".

**For Prosit 3:** ASR decoders can add a language model so that "blood pressure" beats an acoustically similar but unlikely word sequence.

Related: [[perplexity]], [[parameters-vs-hyperparameters]], [[lm-outputs-a-distribution]]
