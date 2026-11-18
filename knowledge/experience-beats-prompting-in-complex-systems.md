---
title: In complex systems, experience finds bugs that prompting alone misses
tags: [ai-use, lecture-11]
source: knowledge/sources/lecture-11.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# In complex systems, experience finds bugs that prompting alone misses

A complex system has many places where things can go wrong, and an AI asked to "fix the bug" does not know where to look. Experience does.

**Example (Lecture 11):** a 10-minute quiz timer ran out in seconds for about three students. The developer, a recent graduate, had spent one to two weeks prompting an AI without finding the cause. In one joint session, experience pointed to it within minutes: the device clock did not match the server's.

**For Prosit 3:** when a model's WER is suddenly bad, check the boring causes first: wrong sample rate (Whisper expects 16 kHz), mismatched text normalisation, or train/test leakage, before changing the model.

Related: [[human-in-the-loop]], [[asr-challenges]], [[measure-before-adding-complexity]]
