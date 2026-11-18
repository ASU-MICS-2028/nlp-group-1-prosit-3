---
title: Reinforcement learning trains an agent to choose actions that maximise reward in an environment
tags: [learning, lecture-06]
source: knowledge/sources/lecture-06.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Reinforcement learning trains an agent to choose actions that maximise reward in an environment

In **reinforcement learning (RL)** an agent acts in an environment. A **state** is a snapshot of the environment, like a room or a chess board. **Actions** change the state and earn **rewards**, such as +1 for winning or reaching a goal. The agent learns to maximise total reward. RL is used in robotics, games and learning from human preferences. Unlike gradient descent on labelled data, the signal often comes only at the end ([[evolutionary-strategies-vs-rl]]).

**Example:** a chess agent gets +1 for a win, −1 for a loss and 0 otherwise. Over many games it learns which moves, many steps earlier, led to wins.

**For Prosit 3:** not used; our ASR models learn from labelled transcripts with supervised losses.

Related: [[preference-data]], [[evolutionary-strategies-vs-rl]], [[alignment-3h]]
