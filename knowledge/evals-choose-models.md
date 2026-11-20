---
title: An eval is a fixed set of prompts with a definition of good output, used to compare models
tags: [evaluation, lecture-10]
source: knowledge/sources/lecture-10.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# An eval is a fixed set of prompts with a definition of good output, used to compare models

To choose a model, build an **eval**: a set of prompts plus a definition of what a good output looks like. Run each candidate on it, compare scores, and rerun when a new model comes out. Later it answers cost questions: "can a $5 model do this $10 job?"

Gamma reportedly makes about 200 LLM calls across 30 to 40 models per deck, picking the best or cheapest model for each subtask.

**Example (Lecture 10):** a student group ran the same tasks on Opus, Sonnet and Haiku. Opus scored about 96%, Haiku lowest in the 80s. The instructor agreed this is essentially an eval.

**For Prosit 3:** our test set is our eval. The RNN and every transformer variant must be scored on the same AfriSpeech test clips with the same [[word-error-rate]] script, so the comparison for Ayamra is fair.

Related: [[model-plus-harness]], [[word-error-rate]], [[ablation-study]], [[save-every-result-to-a-file]]
