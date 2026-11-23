---
title: Speakers dictate punctuation ("comma", "full stop") in a third of the clips, and the references write the marks instead
tags: [M3, data, scoring, dictation]
source: "issue #6; eval/results/m3-whisper-small-zeroshot/"
author: Joseph Etse
ai-use: Claude found the pattern and measured it; Joseph checked the examples
---

# Speakers dictate punctuation ("comma", "full stop") in a third of the clips, and the references write the marks instead

**Question:** why does Whisper add words that are not in the reference?

**What we found:** in 335 of the 1,000 test clips, Whisper writes words like "comma" or "full stop" that the reference does not have. The speakers read the punctuation aloud, exactly as a doctor dictating a note would. The reference writes `,` and `.`, which our scorer removes.

- REF: `Provide pin site care.`
- HYP: `Provide PIN site care. Full stop.`

| Scoring | WER (`whisper-small`, zero-shot) |
|---|---|
| As is | 0.480 |
| Spoken punctuation words removed from the hypotheses | 0.431 |

**Why it matters:**
- Zero-shot models are penalised about 5 WER points for something that is not a recognition error. Fine-tuned models learn to drop these words, so part of their gain over zero-shot is just this.
- For Ayamra it is a feature: doctors will say "full stop", and the demo should turn it into `.`.

**Open:** whether the shared scorer should remove spoken punctuation words on both sides. This changes decision 0009, and Joseph will decide.

**Limits:** "period" and "colon" are also ordinary words (19 references contain one), so removing them blindly from both sides is not quite free.

Related: [[word-error-rate]], [[whisper-zero-shot-loops-on-hard-clips]]
