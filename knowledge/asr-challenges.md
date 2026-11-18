---
title: Domain, vocabulary, noise, sample rate and speaker traits all make ASR harder
tags: [asr, prosit-3]
source: knowledge/sources/lecture-12.md
author: Joseph Etse
ai-use: Claude drafted from the lecture; Joseph reviewed
---

# Domain, vocabulary, noise, sample rate and speaker traits all make ASR harder

From Lecture 12, each one matters for Ayamra:

- **Domain:** medical and legal speech use their own vocabulary, so a general model trips on drug names and conditions. Our test set is half clinical so we can see this.
- **Vocabulary size:** recognising the digits 0–9 is easy; open English is hard; medical English is harder still.
- **Channel and noise:** the instructor described a hospital ASR system built in quiet rooms that failed near a main road; removing the noise took six months.
- **Sample rate:** devices record at different rates (16 kHz vs 8 kHz; the recording says "Hz", almost certainly kHz). A model can work in testing and fail in production. We resample everything to 16 kHz.
- **Speaker traits:** accent, age, gender and region all change the waveform. AfriSpeech has about 120 accents.
- **Code-switching** (mixing English with a local language) is an open research problem. Even Whisper handles it poorly unless its training data covers it.

Related: [[asr-task]], [[afrispeech-200]], [[mel-spectrogram]]
