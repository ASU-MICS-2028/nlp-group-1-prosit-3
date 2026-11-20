---
title: Output tokens cost more than input tokens because generation is one token at a time
tags: [llm-economics, lecture-05]
source: knowledge/sources/lecture-05.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Output tokens cost more than input tokens because generation is one token at a time

LLM APIs charge per million input tokens and per million output tokens. The input (the prompt) is read in parallel. The output is generated **autoregressively**, one token at a time, each step a full pass through the model, so it uses more compute and costs more. Even filler like "please" is billed.

**Worked numbers (Lecture 5, model names garbled):** about $4 in / $20 out per million tokens. A request with 2,000 input and 500 output tokens costs 2,000 × $4/1M + 500 × $20/1M = $0.008 + $0.010 = $0.018, so the shorter output costs more.

**For Prosit 3:** Whisper's decoder is also autoregressive, so transcribing long dictations costs time per output token, while a CTC RNN emits all frames' labels in one pass.

Related: [[positional-embeddings]], [[token-cost-across-languages]], [[ctc]]
