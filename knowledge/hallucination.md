---
title: Hallucination is confident, fluent output that is wrong, because the model fills gaps with likely content
tags: [llm-behaviour, lecture-04]
source: knowledge/sources/lecture-04.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Hallucination is confident, fluent output that is wrong, because the model fills gaps with likely content

When a model lacks the answer, it still produces the most statistically likely words, fluently and confidently. Not all knowledge is in its weights: private files, company databases and the unindexed web were never seen, so questions about them get fluent nonsense.

Lecture 7 showed the same effect in images: a model recolouring a black-and-white Christmas photo added bunting, a clock and a whole new person in an empty gap. It filled empty space with likely pixels, as an LLM fills knowledge gaps with likely words. Even a clear instruction can produce unexpected output, and you only notice if you can check it.

**Example:** ask a chatbot about your company's internal leave policy; it invents a plausible one.

**For Prosit 3:** Whisper is known to sometimes produce fluent text for silence or noise. In a medical note that is dangerous, so our evaluation should look at insertions, not just overall WER.

Related: [[rag]], [[human-in-the-loop]], [[word-error-rate]]
