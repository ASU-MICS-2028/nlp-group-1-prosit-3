---
title: Transformers process all tokens at once, so they need positional embeddings to know word order
tags: [architectures, lecture-05]
source: knowledge/sources/lecture-05.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Transformers process all tokens at once, so they need positional embeddings to know word order

An RNN reads tokens one after another, so order is built in. A transformer processes all tokens **in parallel**, which is why it trains fast on GPUs and why huge training runs are feasible. The cost is that word order is not learned automatically: "dog bites man" and "man bites dog" would look the same.

The fix: each input is **token embedding + positional embedding**, a vector that encodes the token's position.

**Example:** the input for "dog" in position 1 is v(dog) + p(1); in position 3 it is v(dog) + p(3), so the model can tell the two orders apart.

**For Prosit 3:** this parallelism is why Whisper trains faster per hour of audio than an RNN on the same GPU, and why it can handle long clips without the step-by-step bottleneck of [[rnn]].

Related: [[attention]], [[rnn]], [[output-tokens-cost-more]]
