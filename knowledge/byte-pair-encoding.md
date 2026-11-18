---
title: Byte pair encoding builds a subword vocabulary by repeatedly merging the most frequent adjacent pair
tags: [tokenisation, lecture-09]
source: knowledge/sources/lecture-09.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Byte pair encoding builds a subword vocabulary by repeatedly merging the most frequent adjacent pair

**BPE** starts from single characters (or bytes) and repeatedly merges the most frequent adjacent pair into a new token, until the vocabulary reaches a chosen size. Common words become one token; rare words split into known pieces, so there is never an unknown word.

Lecture 2 added a practical rule: tokenizers split text differently, and that is fine **as long as you use one tokenizer consistently** in training and at inference. Lecture 5: preprocessing must fit the task (lowercasing loses the "shouting" of CAPITALS in sentiment).

**Worked example:** corpus "low low lower". Most frequent pair "l o" → merge to "lo"; then "lo w" → "low". Now "low" is one token and "lower" is "low" + "e" + "r".

**For Prosit 3:** Whisper uses a BPE subword vocabulary. Rare clinical or African words split into many tokens, so we should report WER on whole words, not tokens.

Related: [[token-cost-across-languages]], [[perplexity]], [[word-error-rate]]
