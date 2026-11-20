---
title: An agent runs a while loop of plan, act, check until the goal is met
tags: [agents, lecture-08]
source: knowledge/sources/lecture-08.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# An agent runs a while loop of plan, act, check until the goal is met

An agent does what a developer would. For "build me a library backend" it: plans endpoints and data, generates code, writes the files, sets up a database and server, runs the project, tests it against the live endpoints, and if anything fails, finds the bug and goes back to generating code. It is a **`while` loop, not a fixed number of steps**: break when the tests pass. Lecture 10 put it generally: ask the model "what next?", take the step, send back the result, repeat until done.

The loop must also accept new messages while it works. If the user says mid-build "don't add an endpoint for books, I'll load a CSV", that must change what the agent does.

**Example:** run tests → 2 of 10 fail → read errors → fix code → rerun → 10 of 10 pass → stop.

**For Prosit 3:** our training scripts follow a simpler version: train, score WER, adjust, repeat, but with a person deciding when to stop.

Related: [[tools-and-mcp]], [[model-plus-harness]], [[agents-do-long-horizon-work]], [[human-in-the-loop]]
