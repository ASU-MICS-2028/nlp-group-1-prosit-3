---
title: A mel spectrogram turns raw audio into a time-by-frequency picture that models read
tags: [asr, features]
source: knowledge/sources/lecture-12.md; Jurafsky and Martin ch. 16
author: Joseph Etse
ai-use: Claude drafted from the source; to be checked against Jurafsky and Martin ch. 16 (issue #13)
---

# A mel spectrogram turns raw audio into a time-by-frequency picture that models read

Audio is first a **waveform**: thousands of numbers per second (16,000 at 16 kHz), one per sample of air pressure.

**To make a mel spectrogram:**
1. Cut the waveform into short overlapping frames (about 25 ms, every 10 ms).
2. Take each frame's frequency content (a Fourier transform).
3. Group the frequencies into **mel** bands, which are spaced the way human hearing works: fine at low pitch, coarse at high pitch.
4. Take the log.

The result is a matrix: time × about 80 mel bands. It is the input to the M1 BiLSTM and to Whisper. wav2vec2 instead learns its own features straight from the raw waveform with a CNN.

The lecture said libraries produce these for you; you rarely compute them by hand.

Related: [[cnn-is-cross-correlation]], [[rnn]]
