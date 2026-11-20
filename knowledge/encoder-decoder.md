---
title: An encoder-decoder compresses the input into a representation, then generates the output from it
tags: [asr, architectures, M3, M4]
source: knowledge/sources/lecture-12.md; Radford et al. 2023 (Whisper)
author: Joseph Etse
ai-use: Claude drafted from the source; to be checked against Jurafsky and Martin ch. 16 (issue #13)
---

# An encoder-decoder compresses the input into a representation, then generates the output from it

The **encoder** reads the whole input and turns it into a latent representation. The **decoder** generates the output one token at a time, looking at that representation (through cross-attention) and at the tokens it has already written. Encoder-only, decoder-only and encoder-decoder models all exist (Lecture 12).

- **Whisper** is a transformer encoder-decoder: log-mel spectrogram in, text tokens out. It was trained on about 680,000 hours of web audio, so it already "knows" English well before seeing AfriSpeech.
- **Versus CTC:** the decoder acts as a built-in language model, so it spells medical words more consistently. But it can also **hallucinate** fluent text that wasn't said, especially on silence or noise. We check this in the error analysis (M5).
- M3 fine-tunes all of Whisper; M4 fine-tunes it with [[lora]].

Related: [[ctc]], [[rnn]], [[cnn-is-cross-correlation]]
