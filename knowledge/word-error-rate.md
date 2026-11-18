---
title: Word error rate counts the edits needed to turn the model's text into the right text
tags: [asr, evaluation]
source: Jurafsky and Martin ch. 16 (WER); decision 0008 (jiwer)
author: Joseph Etse
ai-use: Claude drafted from the source; Joseph reviewed
---

# Word error rate counts the edits needed to turn the model's text into the right text

**WER = (substitutions + deletions + insertions) / number of words in the reference.** Lower is better: 0 is perfect, and it can go above 1 if the model adds many words.

**Example:** the reference is "the patient has fever" (4 words) and the model says "the patient fever". One word was deleted, so WER = 1/4 = **0.25**.

- **CER** (character error rate) is the same idea counted over characters. It is kinder to near-misses like "hypertension" vs "hipertension".
- **Normalise first.** Lowercase, drop punctuation, collapse spaces. Otherwise "Fever." vs "fever" counts as an error. Our scorer joins "50 s" into "50s" because AfriSpeech's transcripts split them.
- **Corpus-level, not averaged per clip:** add up all the errors and divide by all the reference words. A 2-word clip then can't swing the score.
- We compute it with `jiwer`, the standard library, so our numbers are computed the same way as published ones (decision 0008).

Related: [[afrispeech-200]], [[how-to-score-a-model]]
