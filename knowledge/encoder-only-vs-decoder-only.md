---
title: Encoder-only models classify, decoder-only models generate, encoder-decoders map sequence to sequence
tags: [architectures, lecture-03-part-2]
source: knowledge/sources/lecture-03-part-2.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Encoder-only models classify, decoder-only models generate, encoder-decoders map sequence to sequence

Three architecture families, all mapping source text to a prediction:
- **Encoder-only** (e.g. BERT): encode the input into hidden states, then a small classifier (an MLP) predicts a label such as positive, negative or neutral. BERT is bidirectional, trained by masked-word prediction on both left and right context, though encoders need not be bidirectional.
- **Decoder-only** (GPT-style): no separate encoder. The input is used as context and the model generates text, building its own hidden states.
- **Encoder-decoder:** the encoder builds a representation H and the decoder generates a new sequence from it, e.g. machine translation (see [[encoder-decoder]]).

Turning words into vectors is **encoding**; turning vectors back into language is **decoding**.

**Example:** sentiment of "movie is bad" suits an encoder-only model; "translate to French" suits an encoder-decoder; "continue this story" suits a decoder-only model.

**For Prosit 3:** Whisper is an encoder-decoder (audio in, text out). A CTC RNN is closer to encoder-only: it labels each audio frame with a character.

Related: [[encoder-decoder]], [[rnn]], [[ctc]], [[attention]]
