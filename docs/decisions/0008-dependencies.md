---
title: Dependencies for the shared code: jiwer, huggingface_hub, librosa, pytest
status: Accepted
date: 2026-11-18
decided-by: Joseph
ai-use: Claude proposed; Joseph approved
---

# 0008. Dependencies for the shared code: jiwer, huggingface_hub, librosa, pytest

## Context

S0 (the test set and scorer) needs to compute WER and CER, download the gated dataset, and load audio at 16 kHz. Every new dependency must be justified.

## Options considered

- Write edit distance, download and resampling code ourselves: more code to explain, and our WER might not match published numbers.
- `datasets.load_dataset`: AfriSpeech-200 uses a loading script, which `datasets` 4 and later cannot run.
- jiwer (the standard WER/CER library), huggingface_hub (download files straight from the dataset repo), librosa (load and resample in one call), pytest (tests).

## Decision

jiwer, huggingface_hub and librosa as runtime dependencies; pytest for development. Each model's own libraries (torch, transformers, peft…) are added by its owner with their own decision record.

## Consequences

- Our WER matches how papers compute it.
- Four dependencies to keep up to date. Any new one needs a decision record.
