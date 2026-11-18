---
title: Greedy, top-k, top-p and temperature are ways to pick a token from the distribution at inference
tags: [language-models, lecture-03-part-2]
source: knowledge/sources/lecture-03-part-2.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Greedy, top-k, top-p and temperature are ways to pick a token from the distribution at inference

Decoding only happens at inference; training uses the full distribution.
- **Greedy:** always pick the most likely token. Simple, but can be repetitive.
- **Top-k:** sample from the k most likely tokens, adding variety.
- **Top-p (nucleus):** sample from the smallest set of tokens whose probabilities add up to p.
- **Temperature:** moves sampling between greedy (low) and almost uniform (high).

Lecture 9 warned that top-k and top-p are **sampling methods, not accuracy metrics** (compare [[top-5-accuracy]]).

**Example:** with "to" 0.6, "home" 0.2, "back" 0.1, the rest 0.1: greedy picks "to"; top-2 samples between "to" and "home"; top-p with p = 0.85 samples from {to, home, back} (0.6 + 0.2 + 0.1 = 0.9 ≥ 0.85).

**For Prosit 3:** for dictation we want the single most likely transcript, so greedy or beam search, not random sampling. A doctor's note should not change between runs.

Related: [[lm-outputs-a-distribution]], [[top-5-accuracy]]
