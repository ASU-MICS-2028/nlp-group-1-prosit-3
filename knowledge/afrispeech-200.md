---
title: AfriSpeech-200 is 200 hours of African-accented English, clinical and general
tags: [dataset, asr]
source: https://huggingface.co/datasets/intronhealth/afrispeech-200 (dataset card, read 2026-11-18)
author: Joseph Etse
ai-use: Claude drafted from the source; Joseph reviewed
---

# AfriSpeech-200 is 200 hours of African-accented English, clinical and general

AfriSpeech-200 (Intron Health) is **African-accented English** speech with transcripts: about **200.9 hours**, **67,577 clips**, **2,463 speakers** and about **120 accents** (Yoruba, Igbo, Hausa, Swahili, Zulu, Twi and many more).

| Split | Speakers | Hours | Clips (general + clinical) |
|---|---|---|---|
| train | 1,466 | 173.4 | 58,000 (21,682 + 36,318) |
| dev | 247 | 8.74 | 3,231 (1,407 + 1,824) |
| test | 750 | 18.77 | 6,346 (2,723 + 3,623) |

- **Two domains:** `clinical` (medical sentences, about 62% of clips) and `general`. The clinical part is exactly Ayamra's use case.
- **No speaker appears in more than one split**, so a test score measures how well a model handles new voices.
- **Fields per clip:** `speaker_id, path, audio_id, audio, transcript, age_group, gender, accent, domain, country, duration`.
- **Transcripts space out punctuation** ("in her 50 s ."), so we normalise text before scoring ([[word-error-rate]]).
- **Many accents are tiny** (some have about a dozen clips), so per-accent scores on them are noise. We report accents with 30 or more test clips.
- **Access and licence:** the official repo is gated; we use the public copy `evie-8/afrispeech-200` (decision 0010). CC BY-NC-SA 4.0, for research and non-commercial use. We must not try to identify speakers.
- **Files:** the official repo has `transcripts/<split>.csv` and `audio/<accent>/<split>/*.tar.gz`. The copy we use has Parquet files (`data/<split>-*.parquet`) with the audio inside: train 57,819 clips, dev 3,227, test 6,318 (3,606 clinical, 2,712 general), 28 test clips fewer than the official 6,346. See [[environment]].

**Example:** a Yoruba-accented speaker reading a clinical sentence: "His mother is in her 50 s and has hypertension ."

Related: [[asr-challenges]], [[how-to-score-a-model]]
