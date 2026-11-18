---
name: log-learning
description: Use after comparing two or more ways of doing something, after a run, or after hitting a failure (e.g. "write up what we found", "log this comparison", "that crashed because…"). Writes ONE finding as ONE small file in learnings/, in the simplest words, including the options that lost.
---

# Log a learning

One finding = one file. If you are writing a second heading, it is a second file.

1. **Was it a fair comparison?** Same data, same measure (`common/score.py` on `common/test_set.csv`), same conditions. If not, say so and re-run before logging.
2. **Save the evidence first.** Every number must come from a file in `eval/results/<run>/` (predictions, `scores.json`, `run.md`). Log any GPU run in `docs/gpu-log.md`.
3. **Create** `learnings/<short-slug>.md` from `learnings/TEMPLATE.md`. Set `source` to the issue and the results folder, and fill in `ai-use`.
4. **Write it in the simplest words possible.**
   - The question in one sentence.
   - A table with every option and its numbers, with units. **Losers stay in.**
   - The winner and why, in one sentence a non-expert understands.
   - The limits.

   Link related notes with `[[slug]]`. If a new technical word appears, check that `knowledge/` has a note for it, or write one.
5. **If it led to a choice**, also record a decision (`.claude/skills/new-decision/SKILL.md`) and link this note from it.
6. **Check with your member** that they could explain it in the viva without AI. Run `python3 scripts/build_indexes.py` and commit: `Learning: <title>`.
