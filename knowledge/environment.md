---
title: How to set up your machine for Prosit 3
tags: [setup]
source: README; decisions 0005, 0008; AfriSpeech-200 dataset card
author: Joseph Etse
ai-use: none
---

# How to set up your machine for Prosit 3

1. **Clone the repo and turn on the safety hook:** `git config core.hooksPath .githooks`. It blocks keys, `.env`, audio and model files, and stale indexes.
2. **Python:** install [uv](https://docs.astral.sh/uv/), then run `uv sync`. Always run code with `uv run …`. Add a library with `uv add <name>`, plus a decision record.
3. **Dataset access:** the official AfriSpeech-200 is gated, and our access request is still waiting. For now we use the public copy [evie-8/afrispeech-200](https://huggingface.co/datasets/evie-8/afrispeech-200), which needs no account or token (decision 0010, pending the instructor's approval). `common/data.py` downloads it for you.
4. **Secrets:** `cp .env.example .env` and put any keys in it (an `HF_TOKEN` only if you push checkpoints to the Hub). `.env` is never committed, and assistants are blocked from reading it.
5. **GPU:** one shared account, set up by Joseph (decision 0005). Before a run, write the expected cost in your plan. After it, add a row to `docs/gpu-log.md`.
6. **Load data through `common/data.py`.** `read_split("train", columns)` gives the training rows and `fetch_test_audio()` the test clips, all from one pinned revision so everyone has the same files. The train split is about 55 GB: download it on the GPU machine, not your laptop. See [[how-to-score-a-model]].
7. **GitHub CLI:** `gh auth login`. The skills use `gh` to read issues and open PRs.

Related: [[team]], [[afrispeech-200]]
