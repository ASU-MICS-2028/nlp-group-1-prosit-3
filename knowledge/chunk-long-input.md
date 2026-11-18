---
title: When an API limits input size, split the input into chunks, process each, and join the results
tags: [deployment, lecture-11]
source: knowledge/sources/lecture-11.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# When an API limits input size, split the input into chunks, process each, and join the results

Speech and language APIs cap how much input one call accepts. The standard fix: **chunk** the input, process each chunk, then join the outputs.

**Example (Lecture 11):** a WhatsApp agent turns an uploaded PDF into a voice note. The text-to-speech API limits input size, so it sends the text in chunks and joins the audio. Older models ran sentences together without pauses; newer ones handle pauses themselves, so such workarounds can become unnecessary as models improve.

A related pre-processing idea from the same lecture: for a multi-voice audiobook, an LLM pass first maps each line of dialogue to a character, each character gets a fixed sample voice, and that voice is used throughout.

**For Prosit 3:** Whisper processes 30-second windows, so long dictations must be chunked too. Cutting mid-word can cause errors at the boundaries, so overlapping chunks or cutting at silences is worth testing.

Related: [[asr-challenges]], [[encoder-decoder]], [[experience-beats-prompting-in-complex-systems]]
