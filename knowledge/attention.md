---
title: Attention lets a model weight the words that matter most for the current prediction
tags: [architectures, lecture-05]
source: knowledge/sources/lecture-05.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Attention lets a model weight the words that matter most for the current prediction

The transformer, the backbone of today's LLMs, is built around **attention**: when predicting or representing a token, the model gives more weight to the most relevant other tokens. The attention weights are learned in training like any other parameters.

**Example (Lecture 5):** "The dog could not cross the street because it was too tired / wide." With "tired", the model should attend mostly to "dog" when working out "it" (illustrative weight about 0.7); with "wide", mostly to "street". Working out what "it" refers to is **coreference resolution**. Picking the right meaning of an ambiguous word ("model" as network or as fashion model) is **word sense disambiguation**; attention helps with both.

**For Prosit 3:** attention is the key difference from an RNN. A transformer can look at any audio frame directly, while an RNN must carry everything through its hidden state step by step, which is weaker over long dictations.

Related: [[positional-embeddings]], [[rnn]], [[word-embeddings]], [[encoder-only-vs-decoder-only]]
