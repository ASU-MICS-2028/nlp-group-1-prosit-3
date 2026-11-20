---
title: S0 - fixed 1,000-clip test set, audio access and shared scorer
owner: Joseph Etse
issue: "#3"
pr: "#TBD"
ai-use: Claude Code wrote common/ and its tests from the approved plan and ran the checks; Joseph chose the public dataset copy and reviews the PR
---

# S0: fixed test set, audio access and shared scorer

## What changed

Every model owner can now predict on the same 1,000 test clips and score with one command. See [How to score a model](../../knowledge/how-to-score-a-model.md).

- **`common/test_set.csv`:** 500 clinical and 500 general clips from the AfriSpeech-200 test split, seed 42.
  - Built by `common/build_test_set.py`.
  - Rebuilding gives a byte-identical file.
- **`common/data.py`:**
  - `load_test_set()`, `fetch_test_audio()` and `load_audio()`, which returns 16 kHz mono;
  - `read_split()` for the train and dev splits.
  - Data comes from the public copy `evie-8/afrispeech-200`, pinned to one revision.
- **`common/score.py`:** WER and CER overall, by domain and by accent.
  - It refuses predictions with missing, duplicate or extra IDs.
- **Decisions:**
  - 0009 (test set, scoring, predictions format, checkpoints);
  - 0010 (the public copy, Proposed until the instructor approves).
- **Docs:** the setup docs (`knowledge/environment.md`, `knowledge/afrispeech-200.md`, README, AGENTS.md) now describe the public copy instead of the gated repo.
- **Dependencies:** huggingface_hub, librosa and pyarrow.
- **Tests:** the network test (downloads the audio) is skipped by default. Run it with `uv run pytest -m network`.

## AI use in detail

- **What AI did:** Claude Code (Claude Opus) did the following:
  - wrote the scorer, the data module, the builder and their tests;
  - compared the public copy with the official dataset card;
  - wrote decisions 0009 and 0010 and the scoring note.
- **What the owner did:**
  - found the public copy and asked the instructor about it;
  - decided to build on it while waiting for his reply;
  - approved the plan this follows.
- **How it was checked:**
  - 20 tests pass, including the network test, run once locally on the real audio.
  - Rebuilding the test set gives the same checksum.
  - End to end, hypotheses equal to the transcripts score WER 0.000, and blanking 10 of them scores 0.009.

## Produced

- Decisions: [0009](../decisions/0009-test-set-predictions-and-checkpoints.md), [0010](../decisions/0010-public-mirror-of-afrispeech.md)
- Knowledge: [How to score a model](../../knowledge/how-to-score-a-model.md)
