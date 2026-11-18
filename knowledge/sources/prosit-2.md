---
title: What we did in Prosit 2 (a platform that builds backend APIs) and what carries over
source: Prosit 2 repo, https://github.com/ASU-MICS-2028/nlp-group-1-prosit-2 (README, decisions 0013, 0050, 0051, 0063)
author: NLP Group 1
ai-use: Claude summarised the Prosit 2 repo; numbers copied from its README, which an audit matched to saved result files
---

# Prosit 2: a platform that lets non-developers build backend APIs

## In one paragraph

A non-developer describes a backend in plain words. A Claude coding agent asks up to 3 questions, shows a plan for approval, writes a FastAPI + SQLite backend, tests it in a locked Docker sandbox, and publishes it at a public link. We measured it on a 15-request benchmark with 192 hidden tests. The report had an individual Section A and a shared Section B.

## Key numbers (from the Prosit 2 README, audited against `eval/results/`)

| What | Result |
|---|---|
| Hidden tests passed | Agent 96.0%; one Claude call with no tools 84.0% |
| Asking up to 3 questions first | 96.0% vs 90.1% without |
| One agent vs a Planner/Builder/Tester split | 96.0% at $1.91 vs 87.0% at $4.06 for all 15 tasks |
| Recipe search (RAG), right recipe in the top 3 | Dense (MiniLM) 95%, hybrid 87%, BM25 74%, random 17% |
| Safety | Docker blocked 15 of 16 harmful-code attacks |

## What carries over to Prosit 3

- **Save every result to a file** (P2 decision 0051). A number in the report must come from a saved file. In P2, an audit matched all 105 numbers in the report to files.
- **A relay is slow.** One person at a time left most people waiting (P2 decision 0013), and we switched to everyone working at once (P2 decision 0050). Prosit 3 splits the work by model from day one (decision 0001).
- **Compare against a simple baseline.** "One call with no tools" made the agent's 96% meaningful. In Prosit 3, the RNN baseline and Whisper as it is (zero-shot) play that role.
- **More parts is not always better.** One agent beat a three-agent split on both score and cost. Measure before adding complexity.
- **Keep `main` to what actually runs.** The experiment scripts went to a tag (P2 decision 0063). "Code is liability": the viva can ask about any submitted file.
- **The tooling itself** (secret guards, decision records, skills, `AGENTS.md`) was carried into this repo.
