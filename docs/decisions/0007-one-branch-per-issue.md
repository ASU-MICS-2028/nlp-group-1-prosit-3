---
title: One branch per issue, merged by PR
status: Accepted
date: 2026-11-18
decided-by: Joseph
ai-use: none
---

# 0007. One branch per issue, merged by PR

## Context

Prosit 2 used one branch per relay stage. Prosit 3 work runs in parallel across many issues.

## Options considered

- One branch per person.
- One branch per issue (`<issue#>-<slug>`), merged into `main` by a PR with its change file.

## Decision

One branch per issue. The very first scaffold commit went straight to `main` because the repo was empty.

## Consequences

- Small PRs that are easy to review.
- Each PR maps to one issue and one change file.
