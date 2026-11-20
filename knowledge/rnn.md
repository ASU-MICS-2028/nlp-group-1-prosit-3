---
title: An RNN reads a sequence one step at a time, carrying a hidden state forward
tags: [asr, architectures, M1]
source: knowledge/sources/lecture-12.md; Jurafsky and Martin ch. 8 and 16
author: Joseph Etse
ai-use: Claude drafted from the source; to be checked against Jurafsky and Martin ch. 16 (issue #13)
---

# An RNN reads a sequence one step at a time, carrying a hidden state forward

At each time step t, an RNN combines the current input x_t with its previous hidden state h_{t-1}: **h_t = f(W·x_t + U·h_{t-1} + b)**. The same weights are used at every step, so it handles any length.

- **For speech:** x_t is one frame of the mel spectrogram, and h_t summarises everything heard so far. A layer on top turns each h_t into character probabilities, trained with [[ctc]].
- **LSTM / GRU:** gated versions that keep information over longer spans. Plain RNNs forget, because gradients vanish over many steps.
- **Bidirectional (BiLSTM):** one LSTM reads forwards and one backwards, so each frame sees both past and future context. That suits dictation, where the whole clip is available.
- **Weaknesses for Ayamra:** steps run one after another (slow to train on long audio); long-range memory is weak; and trained from scratch, it has only AfriSpeech's 173 training hours to learn English, while pre-trained transformers bring thousands of hours of prior learning.
- **Strengths:** small, cheap to run, and works on streaming audio.

M1 measures these trade-offs on our test set.

Related: [[ctc]], [[encoder-decoder]], [[data-size-decides-which-model-wins]]
