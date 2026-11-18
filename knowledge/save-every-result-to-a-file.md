---
title: Every number in the report must come from a saved result file
tags: [rules, evaluation]
source: knowledge/sources/prosit-2.md (P2 decision 0051)
author: Joseph Etse
ai-use: none
---

# Every number in the report must come from a saved result file

Any run, comparison or check saves its output in `eval/results/<run>/`: `predictions.csv`, `scores.json` from the shared scorer, and `run.md` saying what model, settings, GPU and cost. Nothing is printed to the terminal and then forgotten.

**Why:** anyone can recheck a number, the report can be written from the results index, and an audit is possible. In Prosit 2, an audit matched all 105 report numbers to files.

Related: [[word-error-rate]], [[code-is-liability]]
