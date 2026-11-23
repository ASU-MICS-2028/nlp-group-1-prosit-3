---
title: torch and transformers for the transformer models
status: Accepted
date: 2026-11-23
decided-by: Joseph
ai-use: Claude proposed; Joseph approved
---

# 0011. torch and transformers for the transformer models

## Context

M2 (wav2vec2), M3 (Whisper) and M4 (Whisper + LoRA) all load pretrained speech models. Every new dependency needs a decision record (AGENTS.md).

## Options considered

- **Hugging Face `transformers` on PyTorch:** has Whisper and wav2vec2 with their processors, a ready speech-recognition pipeline, and `peft` builds on it for LoRA.
- **`openai-whisper`:** covers Whisper only, so M2 and M4 would need other libraries anyway.
- **Writing the models ourselves:** too much code to defend in the viva.

## Decision

Add `torch` and `transformers` to the shared dependencies. They are added once here, so M2, M3 and M4 do not each pick a different version. M4 adds `peft` in its own decision. M1 (the RNN) also uses `torch`.

## Consequences

- `uv sync` now downloads about 1 GB more.
- On the Mac, models run on Apple's GPU (`mps`). On the shared GPU they run on `cuda`. Scripts pick whichever is available.
