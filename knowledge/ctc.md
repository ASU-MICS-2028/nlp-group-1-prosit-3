---
title: CTC lets a speech model learn without anyone marking which sound goes with which letter
tags: [asr, M1, M2]
source: Jurafsky and Martin ch. 16 (Connectionist Temporal Classification, Graves et al. 2006)
author: Joseph Etse
ai-use: Claude drafted from the source; to be checked against Jurafsky and Martin ch. 16 (issue #13)
---

# CTC lets a speech model learn without anyone marking which sound goes with which letter

Audio has far more frames than the transcript has letters, and nobody labels which frame is which letter. **CTC** (Connectionist Temporal Classification) solves this:

1. At every frame, the model outputs a probability for each character, plus a special **blank**.
2. To read off text, **merge repeated characters, then drop the blanks:** `hh_e_ll_ll_oo` → `hello`. A blank between the two `ll` runs keeps the double letter.
3. **Training:** the loss adds up the probability of *every* frame-level path that collapses to the right transcript (computed efficiently with dynamic programming), and the model raises it.

- Used by **M1** (BiLSTM + CTC) and **M2** (wav2vec2 + CTC).
- **Whisper does not use CTC.** It is an [[encoder-decoder]] that writes the text token by token.
- **Weakness:** CTC treats each frame's output as independent, so it has no built-in language model. That can produce misspellings that a decoder or an external language model would fix.

Related: [[rnn]], [[word-error-rate]]
