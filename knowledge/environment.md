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
3. **Dataset access:** AfriSpeech-200 is *gated*. Log in to Hugging Face, open https://huggingface.co/datasets/intronhealth/afrispeech-200 and accept the terms. Then create a read token (Settings → Access Tokens).
4. **Secrets:** `cp .env.example .env` and put your `HF_TOKEN` in it. `.env` is never committed, and assistants are blocked from reading it.
5. **GPU:** one shared account, set up by Joseph (decision 0005). Before a run, write the expected cost in your plan. After it, add a row to `docs/gpu-log.md`.
6. **Do not use `datasets.load_dataset`.** AfriSpeech-200 uses a loading script that `datasets` 4 and later cannot run. Use `common/data.py`, which downloads the files with `huggingface_hub`. See [[how-to-score-a-model]].
7. **GitHub CLI:** `gh auth login`. The skills use `gh` to read issues and open PRs.

Related: [[team]], [[afrispeech-200]]
