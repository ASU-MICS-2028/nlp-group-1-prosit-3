---
title: A languageless LLM would keep knowledge and reasoning in a shared core, with each language as a thin layer
tags: [multilingual, lecture-03-part-1]
source: knowledge/sources/lecture-03-part-1.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# A languageless LLM would keep knowledge and reasoning in a shared core, with each language as a thin layer

Small models (~100M parameters, ~100M training words) already match huge models on syntax and simple semantics. So most parameters in a big model must hold knowledge and reasoning, not language itself. The speaker's idea: learn reasoning in one shared, language-independent core and put each language on top as a thin layer.

The obstacle today is that facts do not transfer between languages. In one experiment, English was duplicated into two identical "copies" with separate tokens. Seeing a fact in the other copy was worth about 70 to 110 times less than seeing it in the same copy.

**Example:** a model that learns "Accra is the capital of Ghana" in English may still not know it when asked in Twi.

**For Prosit 3:** AfriSpeech is English spoken with African accents, so the language is shared; the gap we face is in accent and clinical vocabulary, not facts.

Related: [[token-cost-across-languages]], [[word-embeddings]]
