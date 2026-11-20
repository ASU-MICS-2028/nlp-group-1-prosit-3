# Prosit 3 Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Set up the Prosit 3 repo so five people can each start their model straight away. That means: the guards, generated indexes, the workflow for issues, plans, changes and decisions, the skills, a knowledge folder of atomic notes, the open issues, and S0 (a fixed test set and a shared scorer).

**Architecture:**
- Plain Markdown files with a small frontmatter block.
- One stdlib script regenerates every index file from that frontmatter, so nobody hand-edits a shared index.
- S0 is two small modules in `common/`:
  - `data.py`: the fixed test set and its audio;
  - `score.py`: WER and CER, overall, by domain and by accent.

  Every model writes `predictions.csv` and runs the same scorer.

**Tech Stack:** Python 3.12 via `uv`, pytest, `jiwer` (WER/CER), `huggingface_hub` (download), `librosa` (16 kHz audio), GitHub CLI `gh`.

**Spec:** `docs/superpowers/specs/2026-11-18-prosit-3-setup-design.md`

## Global Constraints

- **Public repo.** Never commit:
  - `.env`, keys or tokens;
  - model files (`*.safetensors`, `*.bin`, `*.pt`, `*.ckpt`, `*.gguf`);
  - audio (`*.wav`, `*.mp3`, `*.flac`, `*.tar.gz`), or anything under `data/` or `models/`;
  - files over 5 MB;
  - raw transcripts, student IDs, emails or phone numbers.
- Python only through `uv` (`uv add`, `uv run`). Every new dependency gets a decision record.
- **Atomic notes:** one idea per file, a frontmatter block with `title`, and `author` and `ai-use` on anything a person wrote. Indexes (`README.md`) are generated and never hand-edited below the `<!-- index -->` marker.
- **Change files** go in `docs/changes/<issue#>-<slug>.md`. Fields: what changed, owner, issue, PR, AI use (which part, which tool, what the person checked), and links to the learnings and decisions it produced.
- **Plan files** go in `docs/plans/<issue#>-<slug>.md`, linked from the issue.
- **Decisions** go in `docs/decisions/NNNN-<slug>.md`, numbered from 0001. Status is one of: Proposed | Accepted | Superseded by NNNN. Include an `ai-use` field.
- **Branches:** one per issue (`<issue#>-<slug>`), merged by PR. The very first scaffold commit (Task 1) goes straight to `main` because the repo is empty.
- **Numbers in the report come only from files in `eval/results/`.**
- **Owners:**

  | Slot | Person | GitHub |
  |---|---|---|
  | M1 | Bernard | `adjeibernardmarfo` |
  | M2 | Alice | `thealiceiris` |
  | M3, S0, setup | Joseph | `josetseph` |
  | M4 | Eric | `ElikplimSunu` |
  | M5 | Michael | `1realMicheal` |

- **Still pending:** whether the report is joint or individual; what counts toward the 10 pages; the deadline; the GPU ceiling. Do not settle these. Leave them in the decision records as `Proposed`.
- **Dataset:** `intronhealth/afrispeech-200` is gated (accept the terms on Hugging Face, then put `HF_TOKEN` in `.env`) and licensed CC BY-NC-SA 4.0. Files: `transcripts/test.csv` (and `transcripts/<accent>/test.csv`), and audio at `audio/<accent>/test/test_<accent>_<n>.tar.gz`. It uses a loading script, which `datasets>=4` cannot run, so we download with `huggingface_hub` and do not use `datasets.load_dataset`.

## Review Focus

1. **A prediction file missing some test IDs, or with duplicates or extra IDs.** The scorer must refuse it with a message naming the IDs. It must not silently score a subset (Task 7 test).
2. **Hypotheses that differ only in case, punctuation or spacing** (`"His mother is in her 50 s ."` vs `"his mother is in her 50s"`). Normalisation must make these equal where we decided they should be (Task 7 test).
3. **An empty hypothesis** (the model output nothing). It counts as all deletions, giving a WER of 1.0 for that clip. It must not crash (Task 7 test).
4. **A note with no frontmatter or no `title`.** The index build fails and names the file. It must not skip the file silently (Task 2 test).
5. **Two parallel PRs creating the same decision number.** The index check fails and names both files (Task 2 test).

---

### Task 1: Repo scaffold and guards (first commit on `main`)

**Files:**
- Create: `.gitignore`, `.env.example`, `pyproject.toml` (via `uv init --bare`), `README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.claude/settings.json`, `.githooks/pre-commit`, `docs/gpu-log.md`
- Create: `scripts/check_secrets.py`, copied from `../nlp-group-1-prosit-2/scripts/check_secrets.py` with `BAD_PATH` extended
- Test: `tests/test_check_secrets.py`

**Interfaces:**
- Produces: `python3 scripts/check_secrets.py --staged|--all`, which exits non-zero and lists problems.

- [ ] **Step 1: Write the failing test.** `tests/test_check_secrets.py`, using `tmp_path` as a throwaway git repo (`git init`, stage files, run the script with `cwd=tmp_path`):
  - `test_blocks_env`: staging `.env` exits 1, and the output contains `.env`.
  - `test_blocks_audio_and_models`: staging `a.wav`, `x.safetensors`, `data/clip.flac` or `audio.tar.gz` exits 1.
  - `test_blocks_hf_token`: a file containing `hf_` plus 34 letters exits 1.
  - `test_allows_csv`: staging `common/test_set.csv` with normal text exits 0.
- [ ] **Step 2:** Run `uv run pytest tests/test_check_secrets.py -v`. Expected: FAIL (the script does not exist).
- [ ] **Step 3: Copy and extend the script.** `BAD_PATH` must also match `\.(bin|pt|ckpt|wav|mp3|flac|tar\.gz)$` and `(^|/)data/`. Keep `MAX_MB = 5`.
- [ ] **Step 4:** Run the tests. Expected: PASS.
- [ ] **Step 5: Write the rest of the scaffold:**
  - `.gitignore`: P2's list plus `data/`, `*.wav`, `*.tar.gz`, `wandb/`, `checkpoints/`.
  - `.env.example`: `HF_TOKEN=`, `GPU_PROVIDER_KEY=` (the name is final once Joseph picks the provider).
  - `.claude/settings.json`: copy from P2, and add `Bash(uv run python -m common.*)` and `Bash(python3 scripts/build_indexes.py*)` to `allow`.
  - `.githooks/pre-commit`: run `check_secrets.py --staged`, then `build_indexes.py --check`. The second line is added in Task 2, so leave it out for now.
  - `docs/gpu-log.md`: a table with the header `| Date | Who | Issue | Provider / GPU | Hours | Cost (USD) | What ran |`.
  - `README.md`: the title, the team, one paragraph on Ayamra, a folder guide matching the spec's layout, and a "Data licence" line: AfriSpeech-200, CC BY-NC-SA 4.0, Intron Health.
  - `AGENTS.md`: adapted from P2's `AGENTS.md`. Keep "How you work: every step, the same way" and the viva and "code is liability" rules as they are. Replace the relay, `PLAN.md` and "stay in your member's stage" with issues, plan files and slots. Replace the "Where things go" table with the spec's layout: knowledge, learnings, plans, changes, decisions and results. List the skills from Task 3.
  - `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`: one line pointing to `AGENTS.md`, as in P2.
- [ ] **Step 6:** Run `git config core.hooksPath .githooks`, then `git add -A && git commit -m "Scaffold repo with secret guards"`. Expected: the hook passes. Then `git push -u origin main`.

### Task 2: Generated indexes

**Files:**
- Create: `scripts/build_indexes.py`, `.github/workflows/checks.yml`
- Modify: `.githooks/pre-commit` (add the `--check` line)
- Create, each with a short intro and the `<!-- index -->` marker: `docs/meetings/README.md` (meeting summaries, `YYYY-MM-DD.md`, not indexed), `knowledge/README.md`, `knowledge/sources/README.md`, `learnings/README.md`, `docs/decisions/README.md`, `docs/changes/README.md`, `docs/plans/README.md`, `eval/results/README.md`
- Test: `tests/test_build_indexes.py`

**Interfaces:**
- Produces:
  - `read_frontmatter(path: Path) -> dict[str, str]`: the flat `key: value` lines between the first two `---` lines. Lists stay as raw strings. It raises `ValueError` naming the file when there is no frontmatter or no `title`.
  - `build(root: Path) -> dict[Path, str]`: maps each index file to its new full text.
  - CLI: `python3 scripts/build_indexes.py` writes the files; `--check` exits 1 and lists the stale ones.
- **Folders and columns.** The first column is always a link to the file, with `title` as the link text. Within a folder, files are sorted by name.

  | Folder | Files | Columns after the link |
  |---|---|---|
  | `knowledge/`, `learnings/` | `*.md` | `tags`, `author` |
  | `knowledge/sources/` | `*.md` | `source` |
  | `docs/decisions/` | `[0-9]*.md` | `status`, `date` |
  | `docs/changes/` | `*.md` | `owner`, `issue`, `ai-use` |
  | `docs/plans/` | `*.md` | `owner`, `issue`, `status` |
  | `eval/results/` | `*/run.md` | `model`, `owner`, `wer` |

  `README.md` and `TEMPLATE*.md` are never indexed. Everything above `<!-- index -->` is kept as it is.

- [ ] **Step 1: Write the failing tests:**
  - `test_index_lists_notes_sorted`: two notes in a temp `knowledge/` produce a table whose rows are in name order, with titles as link text.
  - `test_keeps_text_above_marker`.
  - `test_missing_title_names_file`: `pytest.raises(ValueError, match="bad.md")`.
  - `test_duplicate_decision_number`: `0003-a.md` and `0003-b.md` raise a `ValueError` that names both files.
  - `test_check_detects_stale`: `--check` exits 1 after a note is added without rebuilding.
- [ ] **Step 2:** Run `uv run pytest tests/test_build_indexes.py -v`. Expected: FAIL.
- [ ] **Step 3:** Implement with the stdlib only (`pathlib`, `re`, `argparse`). No YAML library.
- [ ] **Step 4:** Run the tests. Expected: PASS.
- [ ] **Step 5:** Create the index READMEs and run `python3 scripts/build_indexes.py`. Add the `--check` line to the hook. Write `checks.yml` to run `check_secrets.py --all`, `build_indexes.py --check` and `uv run pytest` on push and PR. Add frontmatter to `knowledge/report-format.md` if it is missing any field.
- [ ] **Step 6:** Commit on branch `1-repo-setup`: `"Add generated indexes and CI checks"`.

### Task 3: Workflow templates, skills and first decisions

**Files:**
- Create templates:
  - `docs/decisions/TEMPLATE.md`: P2's `0000-template.md` plus frontmatter `title, status, date, decided-by, ai-use`.
  - `docs/changes/TEMPLATE.md`: frontmatter `title, owner, issue, pr, ai-use`; body sections "What changed", "AI use in detail" (which parts AI did, which tool, what the owner checked), "Produced" (links to learnings and decisions).
  - `docs/plans/TEMPLATE.md`: frontmatter `title, owner, issue, status` (`planned|doing|done`); body sections "Goal", "Steps", "Alternatives to compare", "Failure cases", "GPU cost estimate", "Done when".
  - `knowledge/TEMPLATE.md` and `learnings/TEMPLATE.md`: frontmatter `title, tags, source, author, ai-use`, then one idea in plain words, a real example, and `Related: [[...]]`. A learning adds "Options compared / numbers / winner and why".
- Create GitHub templates: `.github/ISSUE_TEMPLATE/task.yml` (fields: goal, slot label, plan file path, blocked by #, done when) and `.github/pull_request_template.md` (closes #, change file path, checklist: change file written, learnings and decisions added, indexes rebuilt, results saved in `eval/results/`).
- Create skills, adapted from `../nlp-group-1-prosit-2/.claude/skills/`:
  - `start-task`: read the issue, write the plan file from the template, link it on the issue with `gh issue comment`, create branch `<issue#>-<slug>`.
  - `new-decision`: the next free number, from the template.
  - `log-learning`: replaces `log-experiment`. One finding per file, including the options that lost.
  - `finish-task`: check "done when", write the change file, rebuild the indexes, open the PR with `gh pr create`.
  - `summarize-transcript`: lectures go to `knowledge/sources/lecture-NN.md`, then the atomic notes are extracted. Keep P2's privacy grep step exactly.
- Create decisions (status `Accepted` unless marked otherwise; each with Context, Options, Decision, Consequences, taken from the spec):
  - `0001-split-by-model.md`
  - `0002-owners-by-poll.md`
  - `0003-issues-plans-and-change-files.md`
  - `0004-atomic-notes-with-generated-indexes.md`
  - `0005-shared-gpu-account-and-log.md`: `Proposed`; the ceiling and approval rule are pending.
  - `0006-report-format.md`: `Proposed`; joint or individual, and page counting, are pending. It links `knowledge/report-format.md`.
  - `0007-one-branch-per-issue.md`
  - `0008-dependencies.md`: jiwer, huggingface_hub, librosa, pytest; what each replaces and why.
- Create `docs/changes/1-repo-setup.md`, the first change file, covering Tasks 1–3: owner Joseph; AI use: Claude wrote the scaffold, scripts and templates from Joseph's design, and Joseph reviewed them.

- [ ] **Step 1:** Write all the files above.
- [ ] **Step 2:** Run `python3 scripts/build_indexes.py && python3 scripts/build_indexes.py --check`. Expected: exit 0. The decisions index lists 0001–0008, and the changes index lists `1-repo-setup`.
- [ ] **Step 3: Check the skills.** Read each `SKILL.md` and confirm every path it names exists, or is created by that same skill.
- [ ] **Step 4:** Commit `"Add templates, skills and first decisions"`. Open the PR from `1-repo-setup` and merge it once CI is green.

### Task 4: Labels and issues on GitHub (run right after Task 1's push, before Task 2)

GitHub numbers issues and PRs from the same counter. Creating all 17 issues before the first PR keeps the numbers in the table, and the branch names (`1-repo-setup`, `2-knowledge`, `3-s0-…`), correct.

**Interfaces:**
- Produces: issue numbers. Write them into `docs/plans/README.md`'s intro as a "Who does what" table, and into the plan and change files that need them.

- [ ] **Step 1: Check that every owner can be assigned.** Run `gh api repos/ASU-MICS-2028/nlp-group-1-prosit-3/collaborators --jq '.[].login'`. If any owner login from the Global Constraints is missing, stop and ask Joseph to add them. Do not assign issues to people who cannot see the repo.
- [ ] **Step 2: Create the labels** with `gh label create`: `setup, S0, M1, M2, M3, M4, M5, knowledge, section-a, report, slides, reading, pending-confirmation`.
- [ ] **Step 3: Create the issues** with `gh issue create`. Each one gets a body built from the task form; plan file "to be written by start-task" unless stated otherwise.

  | # | Title | Assignee | Labels | Notes |
  |---|---|---|---|---|
  | 1 | Repo setup | Joseph | `setup` | Create it first so the branch name matches. Mark it closed once Task 3's PR merges. |
  | 2 | Knowledge folder | Joseph | `knowledge` | Tasks 5–6 |
  | 3 | S0: test set and scorer | Joseph | `S0` | Tasks 7–8 |
  | 4 | M1 RNN baseline (BiLSTM + CTC) | Bernard | `M1` | Blocked by #3 for scoring only; training can start now |
  | 5 | M2 wav2vec2 fine-tune (CTC) | Alice | `M2` | Same blocker as #4 |
  | 6 | M3 Whisper zero-shot + full fine-tune | Joseph | `M3` | Same blocker as #4 |
  | 7 | M4 Whisper + LoRA | Eric | `M4` | Same blocker as #4 |
  | 8 | M5 Dictation demo | Michael | `M5` | Starts now on zero-shot Whisper |
  | 9 | M5 Error analysis (medical terms, accents) | Michael | `M5` | Uses the `predictions.csv` format from #3 |
  | 10 | M5 Report assembly in the ACL template | Michael | `M5, report` | |
  | 11 | Slides (10 min, GitHub link on slide 1) | Michael | `M5, slides` | Each owner adds their segment |
  | 12 | Section A | Joseph | `section-a, pending-confirmation` | Do not split it until joint vs individual is confirmed |
  | 13–17 | Reading notes | see below | `reading, knowledge` | One source note each in `knowledge/sources/` |

  The reading issues: Jurafsky and Martin ch. 15–17, mainly ch. 16 on RNNs, CTC and ASR (Bernard); wav2vec 2.0, Baevski et al. 2020 (Alice); Liu et al. 2024, Whisper fine-tuning for low-resource ASR (Joseph); Ghimire et al. 2024, PEFT for low-resource ASR (Eric); Sharma et al. 2025, Whisper Tiny for Swahili (Michael).

  Every model issue's "done when":
  - `eval/results/<run>/predictions.csv` and `run.md` exist, and `scores.json` is produced by `common.score`;
  - the learnings notes are written;
  - the Section B subsection draft (about half a page, pending decision 0006) and the slide segment are done;
  - the GPU runs are logged in `docs/gpu-log.md`.
- [ ] **Step 4:** Run `gh issue list -R ASU-MICS-2028/nlp-group-1-prosit-3`. Expected: 17 open issues, each with its assignee. If the numbers differ from the table, update the references in Step 3's bodies.

### Task 5: Knowledge sources (issue #2, branch `2-knowledge`)

**Files:**
- Create in `knowledge/sources/` (frontmatter `title, source, author, ai-use`):
  - `lecture-01.md` … `lecture-08.md`, copied from `../nlp-group-1-prosit-2/knowledge/lectures/` with frontmatter added. Their "Relevance to Prosit 2" sections stay as they are.
  - `lecture-09.md` … `lecture-12.md`, newly summarised with the `summarize-transcript` skill from the lecture transcripts (kept off the repo).
  - `prosit-1.md`, from P2's `knowledge/prosit-1.md`.
  - `prosit-2.md`, new: what we built, the key numbers (taken from P2's README "Results at a glance") and the process lessons.
  - `course.md`, from P2's `knowledge/course.md`, with the out-of-date Prosit 3 dates marked as such.
  - `prosit-3-brief.md`, new: the brief, the deliverables and the rubric, from `~/Downloads/school/Natural Language Processing/Grad NLP Prosit 3.docx (1).pdf` and Lecture 12.

- [ ] **Step 1:** Copy the P2 files and add frontmatter.
- [ ] **Step 2:** Summarise lectures 9–12, one subagent per lecture, each following the skill. Lecture 12 must quote the instructor's report-format and individual-report statements (minutes 63–67).
- [ ] **Step 3: Privacy check** on every new file: `grep -n -E '@|[0-9]{7,}' knowledge/sources/*.md`, then the names grep from the skill. Expected: no hits other than the team and authors of cited papers.
- [ ] **Step 4:** Run `python3 scripts/build_indexes.py --check` (after rebuilding). Expected: exit 0. Commit `"Add knowledge sources: lectures 1-12, prosits, course"`.

### Task 6: Atomic notes, team and environment (issue #2)

**Files:**
- Create in `knowledge/` (one idea each, under about 250 words, linked with `[[...]]`, each naming its source note):
  - The ASR core, from Lecture 12 and the brief: `asr-task.md`, `asr-challenges.md` (domain, vocabulary, noise, sample rate, accent, code-switching), `mel-spectrogram.md`, `cnn-is-cross-correlation.md`, `rnn.md`, `encoder-decoder.md`, `afrispeech-200.md` (from the dataset card, https://huggingface.co/datasets/intronhealth/afrispeech-200: 200.9 h, 67,577 clips, 2,463 speakers, splits 58,000 / 3,231 / 6,346 clips, about 62% clinical), `word-error-rate.md`.
  - Rules and lessons carried over: `cite-claims-not-general-knowledge.md` (Lecture 4), `code-is-liability.md`, `save-every-result-to-a-file.md`, `team-agrees-on-one-recommendation.md` (Lecture 12), and `lora.md` (P1's domain-adapter ranks 2/8/32, with its numbers if `prosit-1.md` has them).
  - Any other concept from Lectures 1–11 that the source notes flag as likely quiz or viva material: one note each.
  - `team.md` (members, slots, GitHub logins, where things live) and `environment.md` (uv, HF token and gated dataset access, GPU account, the hook command).
- Leave `report-format.md` as it is.

- [ ] **Step 1:** Write the notes. Every note's `source` must point to a file in `knowledge/sources/` or to an external URL.
- [ ] **Step 2: Check the links.** Every `[[name]]` must match an existing `knowledge/name.md`: `grep -oh '\[\[[^]]*\]\]' knowledge/*.md | sort -u`, compared with `ls knowledge`. Fix or create the missing ones.
- [ ] **Step 3:** Rebuild the indexes and run the check. Write `docs/changes/2-knowledge-folder.md`. Commit, open the PR, and merge once it is green.

### Task 7: Scorer (issue #3, branch `3-s0-test-set-and-scorer`)

**Files:**
- Create: `common/__init__.py`, `common/score.py`
- Test: `tests/test_score.py`

**Interfaces:**
- **Consumes:** `common/test_set.csv`, with columns `audio_id,transcript,domain,accent,duration` (written by Task 8; tests use a temp file).
- **Produces:**
  - `normalize(text: str) -> str`: lowercase; replace every character that is not a letter, digit, apostrophe or space with a space; join a digit run followed by a lone `s` (`"50 s"` becomes `"50s"`); collapse whitespace; strip.
  - `score(predictions_csv: Path, test_csv: Path = Path("common/test_set.csv")) -> dict`, returning `{"overall": {"wer": float, "cer": float, "n": int}, "domain": {name: {...}}, "accent": {name: {...}}}`. WER is corpus-level (total errors divided by total reference words) via `jiwer`, applied after `normalize`. Accents with fewer than 30 clips are left out of `"accent"`.
  - **Predictions format:** `eval/results/<run-name>/predictions.csv` with columns `audio_id,hypothesis`. Every test ID appears exactly once.
  - **CLI:** `uv run python -m common.score eval/results/<run>/predictions.csv` writes `scores.json` next to the file and prints overall, per-domain and per-accent WER.

- [ ] **Step 1: Write the failing tests:**
  - `test_normalize`: `normalize("His mother is in her 50 s .") == "his mother is in her 50s"`; `normalize("  B.P.  was HIGH!! ") == "b p was high"`.
  - `test_perfect_score`: hypotheses equal to the references give `wer == 0.0` and `cer == 0.0`.
  - `test_known_wer`: the reference `"the patient has fever"` and hypothesis `"the patient fever"` give `wer == 0.25`.
  - `test_empty_hypothesis`: on a 1-clip test set, an empty hypothesis gives `wer == 1.0`, with no exception.
  - `test_by_domain`: a 2-clip test set (one clinical, one general) returns both keys under `"domain"`, each with `n == 1`.
  - `test_missing_ids_refused`: a prediction file without one ID raises a `ValueError` whose message contains that ID.
  - `test_duplicate_or_extra_ids_refused`: the same, for a duplicated ID and an ID not in the test set.
  - `test_small_accent_dropped`: an accent with fewer than 30 clips is not in `"accent"`.
- [ ] **Step 2:** Run `uv run pytest tests/test_score.py -v`. Expected: FAIL.
- [ ] **Step 3:** Run `uv add jiwer`. Implement `common/score.py` with the stdlib `csv` and `json` modules.
- [ ] **Step 4:** Run the tests. Expected: PASS.
- [ ] **Step 5:** Commit `"S0: shared scorer"`.

### Task 8: Fixed test set and audio access (issue #3)

**Files:**
- Create: `common/data.py`, `common/build_test_set.py`, `common/test_set.csv` (generated, committed)
- Create: `docs/decisions/0009-test-set-predictions-and-checkpoints.md`, `knowledge/how-to-score-a-model.md`
- Test: `tests/test_data.py`

**Interfaces:**
- **Consumes:** `HF_TOKEN` from `.env`. Joseph must accept the dataset terms first.
- **Produces:**
  - `load_test_set(path: Path = Path("common/test_set.csv")) -> list[dict]`: the rows of `test_set.csv` as dicts.
  - `fetch_test_audio(dest: Path = Path("data/afrispeech-test")) -> dict[str, Path]`: downloads only the `audio/<accent>/test/*.tar.gz` files for the accents in the test set, extracts them under `dest`, and returns `audio_id → wav/mp3 path` for every test ID. It raises if any ID has no file. It is idempotent: a second call downloads nothing.
  - `load_audio(path: Path) -> numpy.ndarray`: mono float32 at 16 kHz (`librosa.load(path, sr=16000, mono=True)`).
  - Every model owner predicts with this loop: `for row in load_test_set(): hyp = model(load_audio(paths[row["audio_id"]]))`.

- [ ] **Step 1: Look at the real data before writing code.** Download `transcripts/test.csv` with `hf_hub_download(repo_id="intronhealth/afrispeech-200", repo_type="dataset", filename="transcripts/test.csv", token=...)`. Print the columns and 3 rows. Extract one small test tarball and list its paths. Write down:
  - the real column names for ID, transcript, domain, accent and duration;
  - how a tarball path maps to an ID.

  Then use these names in Steps 2–5. If the columns differ from the expected `audio_id, transcript, domain, accent, duration`, `build_test_set.py` renames them to those five, so the interface stays fixed.
- [ ] **Step 2:** `common/build_test_set.py` drops rows with an empty transcript. It then samples **500 clinical + 500 general** clips with `random.Random(42)`, sorted by `audio_id`, and writes `common/test_set.csv`. Run it with `uv run python -m common.build_test_set`. Expected: 1,000 rows, 500 per domain.
- [ ] **Step 3: Write the failing tests.**
  - `test_test_set_shape` (offline): 1,000 rows, the 5 columns, unique IDs, 500 per domain, no empty transcripts.
  - `test_fetch_and_load_audio`, marked `@pytest.mark.network` and skipped when `HF_TOKEN` is unset: fetch the audio, then `load_audio` on the first 3 IDs returns 1-D float32 arrays longer than 0.5 s × 16,000 samples.
- [ ] **Step 4:** Implement `fetch_test_audio` and `load_audio`. Run `uv add huggingface_hub librosa`, then `uv run pytest tests/test_data.py -v`. Expected: PASS, with the network test run once locally with the token.
- [ ] **Step 5: End-to-end check.**
  1. Write a throwaway `predictions.csv` where `hypothesis = transcript` for all 1,000 IDs, under the scratchpad, not in the repo.
  2. Run `uv run python -m common.score <that file>`. Expected: overall WER `0.0`.
  3. Write a second file with the first 10 hypotheses blanked. Expected: WER greater than 0, and per-domain numbers printed.
- [ ] **Step 6: Write decision 0009** (Accepted). It records:
  - the test set: 1,000 clips (500 + 500), seed 42, from the official test split, which keeps speakers separate from training;
  - why a subset: inference cost × 5 models × several runs, while per-domain WER stays stable;
  - the normalisation rules and the 30-clip accent threshold;
  - the predictions format;
  - checkpoints are never committed and are proposed to go on a Hugging Face Hub account for the group (owner Joseph);
  - training and validation use the official train and dev splits, and each owner picks their subset in their own plan;
  - the licence and attribution of the committed transcripts.

  Then write `knowledge/how-to-score-a-model.md`, the copyable predict-and-score recipe from the Interfaces above.
- [ ] **Step 7:** Write `docs/changes/3-s0-test-set-and-scorer.md` and rebuild the indexes. Commit `"S0: fixed test set, audio access, decision 0009"`, open the PR, and merge once it is green. Comment on issues #4–#9 that S0 is ready, with a link to `knowledge/how-to-score-a-model.md`.
