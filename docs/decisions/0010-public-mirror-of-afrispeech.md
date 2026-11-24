---
title: Use the public copy evie-8/afrispeech-200 because official access was not granted
status: Accepted
date: 2026-11-20
decided-by: Joseph; approved by Dr. Asamoah (confirmed to the team 2026-11-24)
ai-use: Claude compared the copy with the official dataset card and wrote the loader; Joseph chose the copy and asked the instructor
---

# 0010. Use the public copy evie-8/afrispeech-200 because official access was not granted

## Context

The official dataset, `intronhealth/afrispeech-200`, is gated. We requested access, and it has not been granted, so no one can start training. A public copy exists at `evie-8/afrispeech-200`. Joseph asked Dr. Asamoah whether we may use it.

## Options considered

- **Wait for official access:** no work can start, with no date.
- **Use the public copy:** available now, no token. We checked it against the official card on 2026-11-20:

  | Split | Copy | Official |
  |---|---|---|
  | Test | 6,318 clips (3,606 clinical, 2,712 general) | 6,346 clips (3,623 clinical, 2,723 general) |
  | Dev | 3,227 clips | — |
  | Train | 57,819 clips | — |

  - The copy has the same columns and the same `speaker/clip` ID format.
  - Its page states no licence. The data is still AfriSpeech-200, so CC BY-NC-SA 4.0 applies.
  - It is stored as Parquet with the audio inside, so `pyarrow` reads it. The official repo's loading script, which `datasets` 4 and later cannot run, is not needed.

## Decision

Use the copy, pinned to revision `cafdc16d1e1dcfcd2b599c00b1ea44d5624db08f`, through `common/data.py`. This adds `pyarrow` to the dependencies in decision 0008.

**Accepted:** Dr. Asamoah approved using the public copy (confirmed to the team on 2026-11-24). If official access is granted later, `common/data.py` (`REPO`, `REVISION` and how the audio is read) could switch to the official files, `common/test_set.csv` would be checked against them, and a new decision would supersede this one.

## Consequences

- The report must name the copy, the pinned revision, and the 28 missing test clips.
- If official access arrives, the 1,000 test IDs can be checked against the official test split. Any ID that is not there would mean rebuilding the test set (a new decision).
