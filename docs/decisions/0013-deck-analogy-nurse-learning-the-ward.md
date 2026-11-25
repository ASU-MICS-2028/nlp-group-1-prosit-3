---
title: The whole deck uses one analogy, a skilled nurse learning a new ward
status: Proposed
date: 2026-11-25
decided-by: Joseph (proposed); the group signs off
ai-use: Claude suggested the analogy in the M3 slide draft; Joseph reviewed it and chose it for the whole deck
---

# 0013. The whole deck uses one analogy, a skilled nurse learning a new ward

## Context

The presentation (#11) is one 10-minute talk with a segment from each member. Past feedback on our decks: they work best when one strong analogy carries the story from the problem to the final results. Each segment needs to fit the same story, so it has to be agreed before people write their slides.

## Options considered

- **One shared analogy: a skilled nurse transferred from abroad learning a new ward at an Ayamra hospital.** She is skilled, but on day one she mishears local names and writes "comma" when the doctor says it; after weeks on the ward she stops. It maps onto every model we built (see Decision).
- **Each speaker picks their own analogy.** Easier to write, but the talk becomes five unconnected stories and the comparison between models gets lost.
- **No analogy, results only.** Shortest, but less educational, and "how educational it was" is part of the presentation grade.

## Decision

Every segment of the Prosit 3 deck fits the nurse-learning-the-ward analogy:

| Segment | In the analogy |
|---|---|
| The problem (Ayamra) | Doctors dictate; someone has to write down what they say |
| M1, RNN from scratch | A new trainee with no experience, trained only on our ward's recordings |
| M2, wav2vec2 | A nurse who has listened to a great deal of speech but never wrote any down, then trained on our ward |
| M3, Whisper zero-shot | The skilled nurse from abroad on day one |
| M3, Whisper fine-tuned | The same nurse after training on our ward's recordings |
| M4, Whisper + LoRA | The same nurse given a short pocket guide for our ward, instead of retraining everything |
| M5, error analysis | The words she still gets wrong: drug names and doses |
| M5, demo | Her first shift taking dictation |

The mapping for M1, M2, M4 and M5 is a proposal; each owner can adjust their line as long as it stays inside the story.

## Consequences

- One story runs from the problem to the recommendation, so the comparison between models is easy to follow.
- Each owner writes their slide to fit their line in the table, and Michael (slides, #11) checks the whole deck for consistency.
- Watch that the analogy does not replace the evidence: every slide still shows the measured numbers.
