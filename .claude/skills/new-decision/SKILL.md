---
name: new-decision
description: Use whenever a choice is made that others should know about, such as an approach, model size, dataset subset, interface, tool, dependency, setting or team rule (e.g. "we'll use whisper-small", "record this decision"). Creates the next numbered decision record in docs/decisions/ and rebuilds the index.
---

# Record a decision

1. **Next number:** the highest number in `docs/decisions/` plus one, four digits (`0012`). Never reuse a number. If another open PR already took it, the index check will fail at merge: renumber yours.
2. **Create** `docs/decisions/NNNN-short-name.md` from `docs/decisions/TEMPLATE.md`.
3. **Fill it in, in plain words:**
   - frontmatter `status`: `Proposed` until the person it affects (or the group, for a team-wide rule) signs off, then `Accepted`;
   - `date`, `decided-by`, and `ai-use`: what AI contributed to the choice, if anything;
   - *Context*;
   - *Options considered*: at least two, with numbers or a link to the `learnings/` note if they were measured;
   - *Decision*;
   - *Consequences*.
4. **Replacing an older decision?** Do not rewrite it. Change only its `status` to `Superseded by NNNN`, and say in the new one which decision it replaces.
5. Run `python3 scripts/build_indexes.py` and commit on the current issue branch: `Decision NNNN: <title>`.
