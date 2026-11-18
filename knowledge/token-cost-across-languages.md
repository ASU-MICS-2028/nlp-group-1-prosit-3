---
title: Languages that split into more tokens cost more compute for the same problem
tags: [multilingual, lecture-03-part-1]
source: knowledge/sources/lecture-03-part-1.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Languages that split into more tokens cost more compute for the same problem

An LLM does one prediction step per token. A language that splits into more tokens (or more Unicode bytes, as non-Latin scripts do) therefore makes the model spend more compute, and more money on per-token pricing, to say the same thing. Byte-level models do not fix this, since bytes are even more numerous. A shared vector space (an "interlingua") could.

**Example:** if an English sentence becomes 10 tokens and its Twi translation becomes 25, the Twi request costs about 2.5 times as many steps, and with [[output-tokens-cost-more]] that difference is billed.

**For Prosit 3:** Whisper's decoder also emits subword tokens. African names, drug names and local words may split into many tokens, which makes them slower to produce and easier to get wrong.

Related: [[byte-pair-encoding]], [[output-tokens-cost-more]], [[languageless-llm]]
