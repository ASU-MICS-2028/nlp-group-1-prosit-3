---
title: A CNN slides a small kernel over the input; it is really cross-correlation
tags: [asr, architectures]
source: knowledge/sources/lecture-12.md
author: Joseph Etse
ai-use: Claude drafted from the lecture; Joseph reviewed
---

# A CNN slides a small kernel over the input; it is really cross-correlation

A **kernel** (a small grid of weights) slides over the input and takes a dot product at each position. A large value means that patch looks like the kernel. The outputs form a new feature map.

- In maths, convolution **flips** the kernel first; CNNs skip the flip. So it is really **cross-correlation**, called convolution "for historical reasons" (Lecture 12).
- **Audio is a 1-D grid** over time, and a spectrogram is a 2-D grid. Either works.
- **CNNs are strong feature extractors:** most speech pipelines start with convolution layers (finding acoustic patterns, phoneme-like pieces) and then pass the features on to an RNN or a transformer. wav2vec2 and Whisper both start with convolutions.
- Deep CNN features are usually not interpretable.

Related: [[mel-spectrogram]], [[rnn]]
