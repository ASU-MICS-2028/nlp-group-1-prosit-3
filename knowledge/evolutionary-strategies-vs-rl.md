---
title: Gradient descent, reinforcement learning and evolutionary strategies are three ways to optimise a model
tags: [training, lecture-03-part-1]
source: knowledge/sources/lecture-03-part-1.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Gradient descent, reinforcement learning and evolutionary strategies are three ways to optimise a model

- **Gradient descent** follows the gradient of the loss directly. It is the most sample-efficient, but costly.
- **Reinforcement learning (RL)** lets the agent choose actions and only gives a reward signal at the end; the model updates from that reward.
- **Evolutionary strategies (ES)** change the weights first (add small random noise), then check whether the reward improved, and keep the changes that helped. They are the least sample-efficient.

The speaker described unpublished work on learning at inference with ES: each server adds tiny noise to its weights (described by one random seed), collects rewards such as "the code ran without error", and every ~1000 steps keeps noise that scored well on average. Only seeds and rewards are shared.

**Example:** RL is like a chess player who plays, then learns from winning or losing. ES is like trying a slightly different player, and keeping it only if it wins more.

**For Prosit 3:** our models are trained with gradient descent on CTC or cross-entropy loss.

Related: [[backprop-and-gradient-descent]], [[reinforcement-learning]], [[chatbots-dont-learn-after-training]]
