---
title: Embeddings turn meaningless token IDs into vectors where similar meanings sit close together
tags: [representations, lecture-03-part-2]
source: knowledge/sources/lecture-03-part-2.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Embeddings turn meaningless token IDs into vectors where similar meanings sit close together

Token IDs are just labels: "The bag is blue" might become 21, 46, 33, 25, and the numbers say nothing about meaning. (Conceptually each ID is a **one-hot** vector.) An **embedding** is a learned vector for each token. In a good embedding space, king, queen and leader sit near each other, and money and bank sit together elsewhere. Embeddings are learned through language modelling: to predict the next word well, the network must build good representations.

- **Static** embeddings (Word2Vec) give "bank" one vector everywhere.
- **Contextual** embeddings (transformers) change with the sentence, so "bank" near "deposited money" differs from "bank" near "river walk". Better representations lead to better predictions.

**Worked example (Word2Vec):** v(king) − v(man) + v(woman) ≈ v(queen).

**For Prosit 3:** the speech encoder plays the same role for audio, turning mel-spectrogram frames into vectors that capture which sound is being spoken.

Related: [[attention]], [[sparse-vs-dense-retrieval]], [[mel-spectrogram]]
