---
title: Knowledge and learnings as atomic notes with generated indexes
status: Accepted
date: 2026-11-18
decided-by: Joseph
ai-use: Claude wrote the index script; Joseph set the rule
---

# 0004. Knowledge and learnings as atomic notes with generated indexes

## Context

Prosit 2 had one long learnings file per person. Long files are hard to search and hard to study for the viva, and five people editing shared index files would cause merge conflicts.

## Options considered

- One long learnings file per person (Prosit 2).
- One idea or finding per file (Zettelkasten), linked with [[slug]], with indexes written by hand.
- The same atomic notes, with indexes generated from each file's frontmatter.

## Decision

Atomic notes in `knowledge/` (what everyone should know) and `learnings/` (what we found while building). Each starts with frontmatter (`title`, `tags`, `source`, `author`, `ai-use`). `scripts/build_indexes.py` rewrites every folder's `README.md` below the `<!-- index -->` line, and the hook and CI fail if an index is stale.

## Consequences

- Notes are small, easy to link and easy to study.
- Nobody edits an index by hand, so there are no conflicts.
- A file without a title fails the check, so notes can't go missing from the index.
