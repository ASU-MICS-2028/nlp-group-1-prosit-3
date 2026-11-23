---
title: Whisper-large-v3-turbo beats whisper-small zero-shot by about 6 WER points, at the same speed on a laptop
tags: [M3, whisper, model-size]
source: "issue #6; eval/results/m3-whisper-small-zeroshot-fallback/, eval/results/m3-whisper-large-v3-turbo-zeroshot-fallback/"
author: Joseph Etse
ai-use: Claude ran both models and wrote the note; Joseph reviews
---

# Whisper-large-v3-turbo beats whisper-small zero-shot by about 6 WER points, at the same speed on a laptop

**Question:** how much does model size alone buy, with no training?

**Options compared and how:** both models zero-shot with temperature fallback and forced English, on the same 1,000 test clips, scored by `common.score`, on an Apple M3 laptop.

| Model | Parameters | WER | Clinical | General | Clips with WER > 1 | Time |
|---|---|---|---|---|---|---|
| whisper-small | 244M | 0.350 | 0.389 | 0.322 | 45 | 1,869 s |
| whisper-large-v3-turbo | 809M | **0.293** | 0.345 | 0.255 | 35 | 1,878 s |

**Winner and why:** turbo. It is more accurate on every domain and every large accent, and it loops less often. It runs at about the same speed, because its decoder has only 4 layers, and decoding is the slow part.

**What did not change:**
- Clinical speech stays about 9 points harder than general speech for both models (drug names, doses, abbreviations).
- Turbo also writes dictated punctuation out as words (378 clips with "comma" or "full stop"). Size does not fix this; fine-tuning should ([[whisper-writes-spoken-punctuation-as-words]]).

**For the fine-tune:** small is the model we planned to fine-tune fully. It is cheap on the GPU, and the comparison with M4 (LoRA) uses the same base. Turbo's zero-shot score of 0.293 is the bar any fine-tuned small model must beat to justify training.

**Limits:** two model sizes only, and no tiny, base or medium. The laptop timings are rough, and the turbo run shared the GPU with a smoke test for a few minutes.

Related: [[whisper-zero-shot-loops-on-hard-clips]], [[encoder-decoder]]
