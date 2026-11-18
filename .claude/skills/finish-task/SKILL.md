---
name: finish-task
description: Use when a member believes their issue is done (e.g. "#4 is finished", "open the PR", "mark this done"). Checks "Done when" really holds, writes the change file (who did what, how AI was used), rebuilds the indexes and opens the PR.
---

# Finish a task

1. **Check "Done when" literally.** Read the checklist in the issue and the plan, and check each item **by running something**, not by assuming. If anything is not true yet, say what is missing and stop.
2. **Check the write-up is complete:**
   - every comparison and failure found has a note in `learnings/`;
   - every choice made has a record in `docs/decisions/`;
   - every reported number has a file in `eval/results/`;
   - every GPU run has a row in `docs/gpu-log.md`.

   Fill any gap now, with your member.
3. **Write the change file** at `docs/changes/<N>-<short-slug>.md` from `docs/changes/TEMPLATE.md`. Ask your member, and do not guess:
   - who was in charge;
   - which parts AI did, with which tool;
   - which parts they did themselves;
   - how they checked the AI's parts.

   Write it honestly; the course AI policy depends on it.
4. **Mark the plan done** (`status: done`). Run `python3 scripts/build_indexes.py` and `uv run pytest -q`. Both must pass. Commit: `Finish #N: <title>`.
5. **Open the PR:** `git push`, then `gh pr create --fill`. Put `Closes #N` and the change file path in the body, following `.github/pull_request_template.md`.
6. **Say what is next:** comment on any issue that was waiting on this one (`gh issue comment M --body "#N is merged: …"`) once it merges.
