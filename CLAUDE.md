@AGENTS.md

## Claude Code specifics

- The step-by-step guides in `AGENTS.md` are also skills: `/start-task`, `/new-decision`, `/log-learning`, `/finish-task`, `/summarize-transcript`.
- `.claude/settings.json` blocks reading `.env` and pre-approves safe commands. Personal settings go in `.claude/settings.local.json`, personal notes in `CLAUDE.local.md` (both git-ignored).
