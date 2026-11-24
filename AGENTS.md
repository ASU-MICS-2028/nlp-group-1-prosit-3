# Instructions for coding assistants

These instructions are for any AI coding assistant working in this repo (Claude Code, Codex, Cursor, Gemini, Copilot and others). `CLAUDE.md`, `GEMINI.md` and `.github/copilot-instructions.md` all point here, so this is the only file to edit.

## The project in two sentences

A team of five students (ICS554 NLP, Ashesi University) is advising Ayamra, a network of African hospitals that wants doctors to dictate their notes. We test the consultant's suggestion (an RNN) against transformer models (wav2vec2, Whisper, Whisper with LoRA) on AfriSpeech-200, recommend one, and build a dictation demo. You are helping **one** member with **their** issue.

## Before you do anything

1. **Find the member's issue.** Run `gh issue list --assignee <their GitHub login>`. Slots and logins are listed in `knowledge/team.md`. Work only on an issue assigned to them. If they ask for something with no issue, help them open one first (`.github/ISSUE_TEMPLATE/task.yml`).
2. **Read, in this order:**
   - `knowledge/README.md`: the index of everything the team knows, starting with `knowledge/sources/prosit-3-brief.md`
   - the issue, and its plan file in `docs/plans/` if it has one
   - `docs/decisions/README.md` and every decision that touches the issue
   - `learnings/README.md`, for findings that others already made on the same problem
3. **Check the safety hook is on:** `git config core.hooksPath` must print `.githooks`. If it prints nothing, run `git config core.hooksPath .githooks`.

## How you work: every step, the same way

Work in small steps. For **each** step:

1. **Explain it first.** Tell your member in plain words what you are about to do and why.
2. **List the diverging paths:**
   - *Alternatives*: other ways to do the same thing (another model size, another learning rate, another library).
   - *Failure cases*: what could go wrong (bad audio, empty transcripts, running out of GPU memory, a run that diverges, the network dropping).
3. **Test as many of them as you can.** Measure alternatives the same way, using `common/score.py` on `common/test_set.csv`, and keep the one that works best.
4. **Explain what happened**, with the numbers, in plain words.
5. **Write it down** (next section). A step is not finished until it is written down.
6. **Commit** on the issue's branch with a message that says what the step did.

Your member must be able to explain and defend every line in the viva **without AI** (course AI policy). Write the **smallest code that works**. The instructor said "code is liability": more code means more to attack and more to explain. Prefer plain code over clever code.

## Where things go

| What | Where | How |
|---|---|---|
| The plan for an issue | `docs/plans/<issue#>-<slug>.md` | From `docs/plans/TEMPLATE.md`, written when the issue starts and linked on the issue |
| One thing you found while building (a comparison, a failure, a number) | `learnings/<slug>.md` | **One finding per file**, in the simplest words, including the options that lost. From `learnings/TEMPLATE.md` |
| One thing everyone should know (a concept, a lecture point, a tool fact) | `knowledge/<slug>.md` | **One idea per file**, linked to other notes with `[[slug]]`. From `knowledge/TEMPLATE.md` |
| A lecture, paper or prosit summary | `knowledge/sources/<slug>.md` | Raw transcripts are never committed |
| A choice others should know about | `docs/decisions/NNNN-<slug>.md` | From `docs/decisions/TEMPLATE.md`. Never edit an old decision away; supersede it |
| What a PR changed, who did it, how AI was used | `docs/changes/<issue#>-<slug>.md` | From `docs/changes/TEMPLATE.md`, **one per PR** |
| Every test result | `eval/results/<run>/` (`predictions.csv`, `scores.json`, `run.md`) | A number in the report must come from here |
| Every run on the shared GPU account | a row in `docs/gpu-log.md` | Say the rough cost before starting the run |
| A meeting | `docs/meetings/YYYY-MM-DD.md` | Summary only |

Every note, learning, plan, decision and change starts with a frontmatter block that includes a `title` and an `ai-use` line. Index files (`README.md` in each folder) are **generated**. After adding files, run `python3 scripts/build_indexes.py`. Never edit below the `<!-- index -->` marker by hand.

## Step-by-step guides

They are written as Claude Code skills, but they are plain Markdown, so any assistant can follow them.

| When | Guide |
|---|---|
| Starting an issue | `.claude/skills/start-task/SKILL.md` |
| You found something (compared options, hit a failure) | `.claude/skills/log-learning/SKILL.md` |
| A choice was made | `.claude/skills/new-decision/SKILL.md` |
| The issue is finished | `.claude/skills/finish-task/SKILL.md` |
| A lecture, meeting or paper needs to go in the repo | `.claude/skills/summarize-transcript/SKILL.md` |

## Rules

- **The repo is public.** Never read, print or commit `.env` or any key. Never commit audio, model weights, `data/`, student IDs or personal details. `scripts/check_secrets.py` runs before every commit and on GitHub, but do not rely on it alone.
- **Stay in your member's slot.** Do not edit code another person owns. If it is broken, say so on their issue.
- **Everyone scores the same way.** Predict on `common/test_set.csv` and score with `uv run python -m common.score`. Never change the test set or the scorer in a model PR. That needs a decision record.
- **Dataset:** AfriSpeech-200, licensed CC BY-NC-SA 4.0, loaded only through `common/data.py` (public copy, decision 0010). Access and setup are in `knowledge/environment.md`.
- **GPU:** one shared account. State the expected cost before a run and log every run in `docs/gpu-log.md`.
- **Python through `uv`** (`uv sync`, `uv add`, `uv run`). Keep dependencies few. Each new one gets a decision record.
- **One branch per issue** (`<issue#>-<slug>`), merged into `main` by a pull request whose change file is filled in.

## Layout

| Path | What | Owner |
|---|---|---|
| `common/` | The fixed test set, audio access and the shared scorer (S0) | Joseph |
| `models/rnn_ctc/` | M1: BiLSTM + CTC baseline | Bernard |
| `models/wav2vec2/` | M2: wav2vec2 fine-tune | Alice |
| `models/whisper_full/` | M3: Whisper zero-shot and full fine-tune | Joseph |
| `models/whisper_lora/` | M4: Whisper + LoRA | Eric |
| `demo/` | M5: dictation demo | Michael |
| `report/` | The ACL-format report and its figures | Michael (assembly), everyone (content) |
| `eval/results/` | Every saved result | Each run's owner |
| `knowledge/`, `learnings/` | Atomic notes and their indexes | Everyone |
| `docs/` | Plans, decisions, changes, meetings, GPU log, design docs | Everyone |
| `scripts/` | `check_secrets.py`, `build_indexes.py` | Joseph |
