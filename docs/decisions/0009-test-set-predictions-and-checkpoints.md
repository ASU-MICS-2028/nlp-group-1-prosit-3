---
title: One fixed 1,000-clip test set, one scorer, one predictions format; checkpoints off the repo
status: Accepted
date: 2026-11-20
decided-by: Joseph
ai-use: Claude wrote the builder and scorer and proposed the numbers; Joseph approved the plan they came from
---

# 0009. One fixed 1,000-clip test set, one scorer, one predictions format; checkpoints off the repo

## Context

Four models (M1–M4) must be compared fairly, and every number in the report has to be traceable to a file. If each owner picked their own test clips or cleaned text their own way, the WERs would not be comparable.

## Options considered

- **The whole test split (6,318 clips, 18.7 hours):** most precise, but running it costs GPU time ×5 models × several runs.
- **A 1,000-clip sample (2.8 hours), half clinical, half general:** cheap enough to re-run after every change, and 500 clips per domain keeps per-domain WER stable.
- **Each owner chooses:** rejected, numbers would not be comparable.

## Decision

- **Test set:** `common/test_set.csv`, built once by `common/build_test_set.py` from the official **test** split (speakers do not overlap with train): drop empty transcripts, then 500 clinical + 500 general with `random.Random(42)`, sorted by `audio_id`. Columns `audio_id, transcript, domain, accent, duration`. Rebuilding gives a byte-identical file.
- **Scoring:** `uv run python -m common.score <predictions.csv>`. Corpus-level WER and CER (jiwer) after normalising both sides: lowercase, keep only letters, digits and apostrophes, collapse spaces, and join "50 s" back into "50s". Reported overall, by domain, and by accent for accents with at least 30 clips.
- **Predictions format:** `eval/results/<run>/predictions.csv` with columns `audio_id,hypothesis`, every test ID exactly once. The scorer refuses missing, duplicate or extra IDs. An empty hypothesis is allowed and counts as all deletions.
- **Train and dev:** each owner trains on the official train split and tunes on dev, choosing their subset in their own plan. The test set is never used for training or tuning.
- **Checkpoints:** never committed. Proposed home: a Hugging Face Hub account for the group, owned by Joseph.
- **Licence:** the committed transcripts are AfriSpeech-200 data (Intron Health, CC BY-NC-SA 4.0), credited in the README.

## Consequences

- Any change to the test set or scorer needs a new decision, and every earlier result must be re-scored.
- Only 5 of the 104 accents reach 30 clips in the sample (Yoruba 100, Swahili 90, Igbo 49, Hausa 35, Zulu 34). Per-accent claims in the report are limited to these.
- The source labels both "zulu" and "isizulu"; we keep the labels as given and say so in the report.
- The data source itself is decision 0010.
