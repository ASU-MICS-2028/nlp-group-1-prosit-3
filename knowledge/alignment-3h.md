---
title: An aligned model is helpful, honest and harmless, and the three can conflict
tags: [alignment, lecture-06]
source: knowledge/sources/lecture-06.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# An aligned model is helpful, honest and harmless, and the three can conflict

The **3H** goals for an aligned assistant:
- **Helpful:** solves the user's real problem.
- **Honest:** accurate, admits uncertainty, does not deceive.
- **Harmless:** no harm to the user, others or society.

They conflict. Being fully helpful with a dangerous request breaks harmlessness. (The summary credits Askell et al., 2021; the transcript does not, so check before citing.)

**Misalignment** is the model doing what it was *told*, not what we *meant*. Lecture 6's analogy: told "get me food" and given money, an agent finds the shop closed and breaks into the kitchen to take food. The instructor called it one of AI's biggest unsolved problems.

**For Prosit 3:** honesty applies to ASR too. A system that flags low-confidence words for the doctor to check is more honest than one that silently guesses a drug name.

Related: [[preference-data]], [[reinforcement-learning]], [[human-in-the-loop]], [[instruction-tuning]]
