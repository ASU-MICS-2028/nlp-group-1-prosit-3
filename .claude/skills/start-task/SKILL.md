---
name: start-task
description: Use when a team member starts work on a GitHub issue (e.g. "start #4", "let's begin my model", "what should I work on"). Checks it is theirs and unblocked, writes the plan file, links it on the issue and makes the branch, before any code is written.
---

# Start a task

Explain each step to your member as you do it.

1. **Find the issue.** If they gave no number, run `gh issue list --assignee <their login>` (logins are in `knowledge/team.md`) and ask which one. Read it with `gh issue view N`. If it is not assigned to them, stop and say so.
2. **Is it unblocked?** Read its "Blocked by". For each `#M`, check that `gh issue view M` is closed, or that the issue says what can start before it (e.g. "train now, score once S0 lands"). Otherwise stop and name what it is waiting on.
3. **Read before building:**
   - `knowledge/README.md`: the notes that touch this issue (and `knowledge/sources/prosit-3-brief.md` if they have not read it);
   - `docs/decisions/README.md`: every decision that touches it;
   - `learnings/README.md`: what others already found on the same problem (for example, another model's data loading).
4. **Make the branch** from an up-to-date `main`: `git switch main && git pull && git switch -c <N>-<short-slug>`. One branch per issue.
5. **Write the plan** at `docs/plans/<N>-<short-slug>.md` from `docs/plans/TEMPLATE.md`, set `status: doing`, and go through it with your member:
   - the steps;
   - for each important step, the **alternatives** worth comparing and how (same data, same measure: `common/score.py` on `common/test_set.csv`);
   - the **failure cases** worth testing;
   - the **GPU cost estimate** for each run (provider, GPU, hours, USD);
   - "Done when", copied from the issue.
6. **Link and commit.** Run `python3 scripts/build_indexes.py`. Commit: `Plan #N: <title>`. Push the branch, then `gh issue comment N --body "Plan: docs/plans/<file> on branch <branch>"`.
7. Work through the plan one step at a time, as `AGENTS.md` describes.
