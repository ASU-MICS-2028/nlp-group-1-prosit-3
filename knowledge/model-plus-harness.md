---
title: An agent is a model plus a harness: the model predicts tokens, the harness gives it tools and a loop
tags: [agents, lecture-10]
source: knowledge/sources/lecture-10.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# An agent is a model plus a harness: the model predicts tokens, the harness gives it tools and a loop

In Lecture 10's analogy the **model** is the car's engine (the intelligence) and the **harness** is the car body: the tools that act (writing files, running code in a sandbox, setting up a database) and the loop around the model. Claude Code and Codex are **harnesses**, not models; each is bundled with a model. Harnesses can be vertical: accounting needs a law-lookup tool, Gamma is a slides harness.

A **framework** (LangChain, LangGraph, Google ADK) is a toolkit for building your own harness; a ready-made harness is a generic loop you just use (Lecture 8).

**A good harness can lift a weaker model.** Illustration: a strong model alone writes correct code 85% of the time. A weaker one manages 70%, but its harness runs the code in a sandbox and sends errors back for a retry, reaching about 95%.

**For Prosit 3:** the same holds for ASR: post-processing (a medical word list, a doctor review step) around a smaller model may beat a bigger model used bare.

Related: [[agent-loop]], [[tools-and-mcp]], [[evals-choose-models]]
