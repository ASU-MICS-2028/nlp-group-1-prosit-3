---
title: Repo setup - guards, generated indexes, workflow templates, skills, decisions 0001-0008
owner: Joseph Etse
issue: "#1"
pr: "#18"
ai-use: Claude Code wrote the scaffold, scripts, templates and skills from Joseph's design; Joseph reviewed them
---

# Repo setup

## What changed

- `scripts/check_secrets.py` (from Prosit 2, extended to block audio, model files and `data/`) runs in the pre-commit hook and on GitHub.
- `scripts/build_indexes.py` regenerates every folder's `README.md` index from frontmatter. The hook and CI fail when an index is stale, when a note has no title, or when two decisions share a number.
- Templates for plans, changes, decisions, knowledge notes and learnings; a GitHub issue form; a PR template.
- Skills: `start-task`, `new-decision`, `log-learning`, `finish-task`, `summarize-transcript` (adapted from Prosit 2).
- Decisions 0001-0008. `AGENTS.md`, `README.md`, `docs/gpu-log.md`, `.env.example`.
- Issues #1-#17 created and assigned.

## AI use in detail

- **What AI did:** Claude Code (Opus) drafted the design doc and plan with Joseph, and wrote every file in this PR and its tests.
- **What Joseph did:** chose the workflow rules (issues, change files, atomic notes), the split by model and the owners (by poll), and reviewed the design, the plan and this PR.
- **How it was checked:** 10 tests (`uv run pytest`) covering the guards and the index builder. The hook ran on every commit.

## Produced

- Decisions: [0001](../decisions/0001-split-by-model.md) to [0008](../decisions/0008-dependencies.md)
- Design: `docs/superpowers/specs/2026-11-18-prosit-3-setup-design.md`; plan: `docs/superpowers/plans/2026-11-18-prosit-3-setup.md`
