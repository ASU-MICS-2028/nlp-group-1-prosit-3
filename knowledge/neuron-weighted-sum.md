---
title: A neuron outputs a weighted sum of its inputs, and a model is just its learned weights
tags: [neural-networks, lecture-01]
source: knowledge/sources/lecture-01.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# A neuron outputs a weighted sum of its inputs, and a model is just its learned weights

A neuron takes inputs x_i, gives each a weight w_i (how much it matters) and outputs the **weighted sum y = Σ x_i · w_i**. Connect many neurons in layers, each output feeding the next, and you get a **feed-forward network**. Wider means more neurons per layer; deeper means more layers.

The weights are not written by hand. They are learned from examples, and the trained model *is* those weights: a long list of numbers (about 175B for GPT-3.5, as looked up in class). Which numbers a model has is called its **parameters**.

**Example (Lecture 1):** predict student success from (attendance /100, assignments /10, a yes/no factor). Student A is (50, 6, 1) and B is (60, 5, 1). With weights (0.1, 1, 2), A scores 5 + 6 + 2 = 13 and B scores 6 + 5 + 2 = 13, a tie; change the weights and either can win. The weights come from past students' records.

**For Prosit 3:** "RNN vs transformer" is a choice of how neurons are arranged (the architecture); both are trained the same way, by learning weights from AfriSpeech audio.

Related: [[parameters-vs-hyperparameters]], [[backprop-and-gradient-descent]], [[rnn]]
