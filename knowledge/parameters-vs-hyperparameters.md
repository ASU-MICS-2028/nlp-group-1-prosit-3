---
title: Parameters are learned from data; hyperparameters are chosen by you and tuned by trial
tags: [training, lecture-02]
source: knowledge/sources/lecture-02.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Parameters are learned from data; hyperparameters are chosen by you and tuned by trial

**Parameters** are the weights the model learns during training. **Hyperparameters** are the settings you pick before training: width (neurons per layer), depth (number of layers), learning rate, and N in an n-gram model. No theory gives you the right hyperparameters, so you try values and compare (Lecture 4 told of a model that only trained once the right learning rate was found).

To judge a setting, read the output first, then use a proper metric such as [[perplexity]] or [[word-error-rate]].

**Example:** in an n-gram model the probabilities are parameters, counted from the corpus; N = 3 is a hyperparameter you chose.

**For Prosit 3:** LoRA rank, learning rate and number of RNN layers are hyperparameters. Each one we try should be logged with its WER so the comparison is fair.

Related: [[neuron-weighted-sum]], [[ablation-study]], [[lora]], [[save-every-result-to-a-file]]
