---
title: A speech encoder's lower layers learn sounds shared by all languages, so fine-tuning can leave them frozen
tags: [fine-tuning, whisper, M3]
source: knowledge/sources/liu-2024-whisper-fine-tuning.md
author: Joseph Etse
ai-use: Claude drafted from the paper; Joseph reviewed
---

# A speech encoder's lower layers learn sounds shared by all languages, so fine-tuning can leave them frozen

In a deep speech encoder, layers near the input capture basic sounds that all human speech shares, because everyone's mouth makes sounds the same way. Layers near the top capture features specific to one language.

Liu et al. (2024) checked this on Whisper-large-v2. They compared each encoder layer before and after fine-tuning:
- the bottom ~15 of 32 layers hardly changed;
- the top layers changed most.

Freezing the bottom 10–20 layers while fine-tuning gave slightly *better* WER than updating everything: 16.3% against 17.4%, averaged over seven languages. It also trained fewer weights.

**Example:** to adapt Whisper to Nigerian-accented clinical English, the lower layers already hear the sounds correctly. The upper layers need to learn the accent's patterns and the medical words.

Related: [[encoder-decoder]], [[catastrophic-forgetting]], [[liu-2024-whisper-fine-tuning]]
