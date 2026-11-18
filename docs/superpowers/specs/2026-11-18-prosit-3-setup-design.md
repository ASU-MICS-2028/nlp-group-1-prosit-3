# Prosit 3 setup: repo, workflow and work split

- Date: 2026-11-18
- Status: Draft, waiting for approval

## Intent and the why

Prosit 3 (ICS554, Ashesi) asks us to act as AI technologists for Ayamra, a fictional network of African hospitals that wants doctors to dictate their clinical notes. A consultant told Ayamra to use RNNs and the AfriSpeech-200 dataset. We must:

1. explain RNNs and how they could solve this;
2. weigh RNNs against other approaches;
3. recommend an approach (the prosit title, "Supervised Speech Recognition with Transformers", points to transformers);
4. build the recommended system and evaluate it.

Deliverables are an ACL-style report under 10 pages, a 10-minute team presentation, and the code on GitHub, with the repo link on page 1 of both the report and the slides. Grading: presentation 20%, report Section A 20%, report Section B 25% (implementation and results 20%, writing 5%), and a viva quiz 35%.

This document sets up **how the team works**, not the model details. The aims are:

- every task can be done without waiting on someone else, unless that is unavoidable;
- every decision and change is traceable, with who did it and how AI was used;
- everyone can defend the whole system in the viva.

## Goals

- A public repo, `ASU-MICS-2028/nlp-group-1-prosit-3`, carrying over what worked in Prosit 2: the secret-blocking pre-commit hook, decision records (ADRs), the AGENTS.md rules for coding assistants, the skills and the "save every result to a file" rule.
- **GitHub issues for all work.** Each issue has a plan file at `docs/plans/<issue#>-<slug>.md`, linked from the issue.
- **A change log.** Each change gets its own file in `docs/changes/` saying what changed, who was in charge, the issue, and how AI was used (which part, which tool). An index file lists every change.
- **Atomic notes (Zettelkasten).** Knowledge and learnings are small files, one fact, procedure or approach each, linked to each other, with an index file per folder.
- **A knowledge folder** built from everything so far: lectures 1–11, Prosit 1, Prosit 2 and the course.
- **The work split by model** (approved):

| Slot | Owner | Owns end to end |
|---|---|---|
| M1 | Bernard | RNN baseline: BiLSTM trained with CTC, the consultant's suggestion, actually tested |
| M2 | Alice | wav2vec2 fine-tuned with CTC |
| M3 | Joseph | Whisper, full fine-tune (and the zero-shot Whisper baseline) |
| M4 | Eric | Whisper with LoRA (parameter-efficient fine-tuning) |
| M5 | Michael | Dictation demo, error analysis (medical terms, accents), report and slide integration |

  Slots were picked by poll. Joseph also owns every shared bottleneck task by default: the setup and S0.

  One shared task comes first: **S0 (fixed test split and scorer)**. Its interfaces go in a decision record on day 1. After that, M1–M4 run fully in parallel. M5 builds the demo against any checkpoint (zero-shot Whisper works from day 1) and the error analysis against the prediction-file format, so M5 does not wait either.
- Each model owner writes the Section B subsection and the slide segment for their model. Section A is written by each person alone, as in Prosit 2.

## Non-goals

- Model hyperparameters, dataset subset sizes and GPU provider choices. Each model owner decides these in their own issue plan and records them as a decision.
- A production deployment for Ayamra. The demo only shows the idea.
- Copying Prosit 2's relay and `PLAN.md`. Issues replace them.

## Anti-goals (a failure even if it technically works)

- A number in the report that does not come from a saved file in `eval/results/`.
- Code a member cannot explain without AI in the viva ("code is liability": write the smallest code that works).
- Raw lecture or meeting transcripts, keys, `.env` files, student IDs or personal details committed to the public repo.
- Atomic notes that are actually long essays, or notes that never get indexed.
- Five people blocked on one person's data pipeline.

## Constraints

- Public repo. The course AI policy requires each member to defend their own work without AI.
- GPU: one **shared** cloud account (RunPod, Modal, AWS or similar), set up by Joseph. The key lives only in each member's git-ignored `.env`, with `.env.example` committed. Each owner states the expected cost in their issue plan before a run, and every run gets one row in `docs/gpu-log.md`: who, issue, GPU, hours, cost. The spending ceiling and the approval rule go in a decision record when Joseph sets up the account.
- Python through `uv`, as in Prosit 1 and 2. Few dependencies; each new one gets a decision record.
- Dataset: `intronhealth/afrispeech-200` on Hugging Face (accented English, clinical and general domains, about 120 accents).
- Deadline: not yet set; the course outline's Nov 20 date is out of date.
- Five members, the same as in Prosit 2: Michael Boadi, Joseph Etse, Alice Kara-Acquah, Bernard Marfo, Eric Sunu.

## Approaches considered (for splitting the work)

- **By pipeline stage** (data / RNN / Whisper / eval / demo, with interfaces fixed up front). Each part gets one deep owner, but a slow upstream stage stalls the others, and each person knows one slice only, which is weak for a 35% viva.
- **By model, end to end (chosen).** It needs only one tiny shared task (S0). The results table becomes the report's argument: RNN against transformers on the same data. Everyone learns the full ASR pipeline. The cost is some repeated setup, softened by shared learnings notes.

## The design

### Repo layout

```
README.md                  what this is, results at a glance, how to run, folder guide
AGENTS.md                  rules for any coding assistant (CLAUDE.md, GEMINI.md, copilot point here)
knowledge/                 shared notes, one idea per file; README.md is the index
  sources/                 one summary per lecture / prosit / paper (literature notes)
  *.md                     atomic notes, e.g. ctc-loss.md, word-error-rate.md, afrispeech-200.md
learnings/                 what we found while building, one finding per file; README.md is the index
docs/
  plans/                   one plan per issue: <issue#>-<slug>.md
  decisions/               ADRs, NNNN-<slug>.md, README.md is the index
  changes/                 one file per merged PR: NNNN-<slug>.md, README.md is the index
  meetings/                meeting summaries
common/                    S0: data split loader + score.py (WER/CER, overall, by domain, by accent)
models/rnn_ctc/            M1
models/wav2vec2/           M2
models/whisper_full/       M3
models/whisper_lora/       M4
demo/                      M5
eval/results/              every result file + README.md index (numbers in the report come only from here)
report/                    Section B source and figures
scripts/                   check_secrets.py, build_indexes.py
.claude/skills/            the step-by-step guides
.githooks/, .github/       pre-commit hook, PR template, CI checks
```

Slides live in the shared Drive as a `.pptx` (team habit), with a link in the README.

### Atomic notes (knowledge and learnings)

Every note is one file with a short frontmatter:

```markdown
---
title: CTC loss lets a model learn alignment it was never given
tags: [asr, rnn]
source: knowledge/sources/lecture-xx.md | issue #12
author: <name>
ai-use: none | "Claude drafted the explanation; checked against J&M ch. 16"
---
One idea, in plain words, with a real example. Links: [[word-error-rate]], [[bilstm]].
```

- `knowledge/` holds what everyone should know: course concepts, the dataset and tools.
- `learnings/` holds what we found by doing it: comparisons with numbers, failure cases and the options that lost.
- `scripts/build_indexes.py` regenerates every `README.md` index (knowledge, learnings, decisions, changes, results) from the frontmatter, so five people adding notes in parallel never hand-edit a shared index. CI fails if an index is stale.

### Issues, plans and changes

- **Issue** = a unit of work, assigned to one person. Labels: `S0`, `M1`–`M5`, `section-a`, `knowledge`, `report`, `slides`, `setup`. An issue form asks for the plan file link and any "blocked by #N".
- **Plan file** = written at the start (by the `start-task` skill): steps, alternatives to compare, failure cases, the "done when" check, and the expected GPU cost.
- **Change file** = written in the PR that closes the issue (by the `finish-task` skill): what changed, who was in charge, the issue/PR link, AI use (which parts AI did, which tool, what the person checked), and links to the learnings and decisions it produced. The PR template has the same fields, so nothing merges without one.
- **Decisions** keep the Prosit 2 ADR format, plus an `AI use` line.
- **Branches:** one per issue (`12-rnn-baseline`), merged by PR. This differs from Prosit 2's one branch per stage, because the work now runs in parallel and is not a relay.

### Skills (carried over and adapted)

`start-task` (reads the issue, writes the plan file), `new-decision`, `log-learning` (replaces `log-experiment`: one atomic file per finding), `finish-task` (writes the change file, closes the issue), `summarize-transcript` (writes to `knowledge/sources/`, then extracts atomic notes). `handoff` is dropped (no relay).

### First issues to open

1. Setup: repo scaffold, `.env.example`, `docs/gpu-log.md`, hook, CI, indexes, templates, skills (Joseph, with Claude).
2. Knowledge: lecture 1–11 sources + atomic notes; Prosit 1 and 2 sources; assignment and course notes.
3. S0: fixed test split and scorer, plus the prediction-file format as a decision record.
4. M1–M4: one issue per model (training + predictions on the S0 split + Section B subsection + slides).
5. M5: demo; error analysis; report and slide integration.
6. Section A: one issue per person.
7. Readings: Liu et al. 2024, Sharma et al. 2025, Ghimire et al. 2024. One source note each, spread across people.

## Calls made after the builder check (correct any)

- **Report format: PENDING confirmation.** Joseph says the report is joint. In Lecture 12 the instructor said it is individual (Section A individual plus Section B), but promised to confirm with the brief's author. Until that is confirmed, `report/` uses the official ACL template (see `knowledge/report-format.md`) and M5 assembles the PDF. If the report is joint, Section A is one shared text split by topic across members; if it is individual, each member writes their own Section A outside the repo. Also open: whether references and Limitations count toward the 10 pages.
- **Checkpoints:** model files never go in the repo. The S0 decision record also fixes where they live (proposed: one Hugging Face Hub repo per model, under a group account) so that M5 and the viva can reload them.
- **No deadline yet:** issues carry no dates. Each model plan starts with a minimum version (for example, a small fine-tune on a subset) before the full run, so a short deadline still gives every slot a result. When a date is set, it goes in a decision record and becomes a GitHub milestone.

## Left to the builder

- Exact frontmatter fields and the index format, as long as they are generated, not hand-edited.
- CI details and the hook implementation (reuse Prosit 2's).
- The wording of the issue forms, the PR template and the skills.
- Which notes get extracted from each lecture.
