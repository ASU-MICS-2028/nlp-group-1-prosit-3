---
title: Split the work by model, each person end to end
status: Accepted
date: 2026-11-18
decided-by: Joseph, agreed by the group
ai-use: Claude laid out the options; Joseph chose
---

# 0001. Split the work by model, each person end to end

## Context

Prosit 3 asks us to judge the consultant's RNN advice and build the recommended system. Five people need to work at the same time without waiting on each other, and everyone faces a 35% viva on the whole system.

## Options considered

- By pipeline stage (data / RNN / Whisper / eval / demo) with interfaces fixed up front: one deep owner per stage, but a slow upstream stage blocks the rest, and each person knows only one slice.
- By model, end to end: after one small shared task (S0: test set and scorer), each person trains, predicts and scores one model on their own.

## Decision

By model. Slots: M1 RNN baseline (BiLSTM + CTC), M2 wav2vec2 (CTC), M3 Whisper zero-shot and full fine-tune, M4 Whisper + LoRA, M5 demo, error analysis and integration. S0 comes first and is the only shared dependency.

## Consequences

- The results table is the report's argument: RNN against transformers on the same 1,000 test clips.
- Everyone learns the whole ASR pipeline (audio in, text out, WER), which helps in the viva.
- Some setup is repeated across models. Learnings notes share what one person found, so others don't hit it again.
