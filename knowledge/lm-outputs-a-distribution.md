---
title: A language model outputs a probability distribution over the vocabulary, not a single token
tags: [language-models, lecture-03-part-2]
source: knowledge/sources/lecture-03-part-2.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# A language model outputs a probability distribution over the vocabulary, not a single token

At each step a language model gives every token in its vocabulary a probability, and these add up to 1. It does not output a word. A good model puts high probability on the correct next token; if the right answer "to" gets only 0.01, the model is wrong.

During **training** only this distribution matters: it is compared with the ground truth using [[cross-entropy-loss]], and nothing is sampled. At **inference** you must turn the distribution into a token (see [[decoding-strategies]]). Decoding is a loop: after "I am going to", the chosen "to" is added, and the model predicts again for "school".

**Example:** after "I am going", a model might give "to" 0.6, "home" 0.2, "back" 0.1, and spread the remaining 0.1 over the rest of the vocabulary.

**For Prosit 3:** an ASR model does the same per audio frame (CTC) or per output token (Whisper's decoder), giving probabilities over characters or subword tokens.

Related: [[cross-entropy-loss]], [[decoding-strategies]], [[ctc]]
