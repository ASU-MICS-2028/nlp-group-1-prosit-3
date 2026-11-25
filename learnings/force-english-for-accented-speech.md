---
title: Telling Whisper the speech is English beats letting it guess, by 11 WER points
tags: [M3, whisper, decoding]
source: "issue #6; eval/results/m3-whisper-small-zeroshot-fallback/, eval/results/m3-whisper-small-zeroshot-fallback-detect/"
author: Joseph Etse
ai-use: Claude ran both settings and wrote the note; Joseph reviews
---

# Telling Whisper the speech is English beats letting it guess, by 11 WER points

**Question:** should Whisper detect the language itself, or be told the speech is English?

**Options compared and how:** whisper-small zero-shot with temperature fallback, same 1,000 test clips, scored by `common.score`. Only the language setting differs.

| Option | WER | Clinical | General | Clips with WER > 1 | Clips not in Latin script |
|---|---|---|---|---|---|
| **Forced English** | **0.350** | 0.389 | 0.322 | 45 | 0 |
| Language detected | 0.464 | 0.516 | 0.426 | 75 | 66 |

**Winner and why:** forced English. With detection, Whisper decided some accented English clips were another language and wrote them in Arabic, Bengali or Georgian script, or looped. Every AfriSpeech clip is English, so there is nothing to detect.

**Limits:** one model (small), zero-shot only. The detection run was also 4.6 times slower on the GPU than the fine-tuned model's prediction (4,032 s against 878 s), but the two runs used different checkpoints.

Related: [[whisper-zero-shot-loops-on-hard-clips]], [[bigger-whisper-helps-zero-shot]]
