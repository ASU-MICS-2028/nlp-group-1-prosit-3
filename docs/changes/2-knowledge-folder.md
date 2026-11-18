---
title: Knowledge folder - lectures 1-12, prosits, course, 61 atomic notes
owner: Joseph Etse
issue: "#2"
pr: "see PR"
ai-use: Claude Code summarised lectures 9-12 from the transcripts and wrote the atomic notes; Joseph reviewed samples. Lectures 1-8 were carried over from Prosit 2
---

# Knowledge folder

## What changed

- `knowledge/sources/`: summaries of lectures 1-12 (1-8 carried over unchanged from Prosit 2, 9-12 new); Prosit 1 and Prosit 2 recaps; the course outline (its Prosit 3 dates marked out of date); the Prosit 3 brief.
- `knowledge/`: 61 atomic notes, one idea each, linked with `[[slug]]`:
  - speech recognition: ASR task and challenges, mel spectrograms, CNNs, RNNs, CTC, encoder-decoder, WER, AfriSpeech-200;
  - every quiz or viva concept flagged in lectures 1-11;
  - rules and lessons carried over: code is liability, save every result, citations, one shared recommendation, measure before adding complexity;
  - `team.md` and `environment.md`.
- Every `[[link]]` resolves, except `[[how-to-score-a-model]]`, which arrives with S0 (#3).

## AI use in detail

- **What AI did:** Claude Code (Opus) agents summarised lectures 9-12 from the raw transcripts using the `summarize-transcript` skill, and extracted 43 concept notes from the lecture summaries. Claude wrote the 18 Prosit 3 and ASR notes, the Prosit 2 recap and the brief summary.
- **What Joseph did:** chose the scope, and reviewed the Lecture 12 quotes against the transcript and a sample of notes.
- **How it was checked:** a privacy grep for names, emails and long numbers on every new source; a link check; the index check. Notes that use textbook definitions or made-up examples say so. **Check any note against its source before citing it in the report.**

## Produced

- `knowledge/README.md` and `knowledge/sources/README.md` indexes.
