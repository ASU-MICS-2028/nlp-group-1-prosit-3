---
title: GitHub issues, one plan per issue, one change file per PR
status: Accepted
date: 2026-11-18
decided-by: Joseph
ai-use: Claude drafted the templates and skills; Joseph set the rules
---

# 0003. GitHub issues, one plan per issue, one change file per PR

## Context

Prosit 2 tracked work in `docs/PLAN.md` with a relay order. Prosit 3 work runs in parallel, and the course needs a clear record of who did what and how AI was used.

## Options considered

- Keep a single PLAN.md table.
- GitHub issues for all work, each with a plan file, and a change file for every merged change saying who did it and how AI was used.

## Decision

Every unit of work is a GitHub issue assigned to one person. The `start-task` skill writes `docs/plans/<issue#>-<slug>.md` and links it on the issue. The `finish-task` skill writes `docs/changes/<issue#>-<slug>.md` (what changed, owner, issue, PR, AI use) and opens the PR. The PR template asks for both.

## Consequences

- Progress is visible on GitHub, not in one file that everyone edits.
- The AI-use record is written per change, while it is still remembered.
- Change files are named by issue number, so parallel PRs never clash.
