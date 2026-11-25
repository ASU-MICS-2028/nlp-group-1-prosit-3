---
title: Reading note on Liu et al. 2024 (Whisper fine-tuning strategies for low-resource ASR)
owner: Joseph Etse
issue: "#15"
pr: "#TBD"
ai-use: "Claude Code downloaded the paper and drafted the three notes from the PDF and Joseph's summary; Joseph read the paper and the notes"
---

# Reading note on Liu et al. 2024

## What changed

- `knowledge/sources/liu-2024-whisper-fine-tuning.md`: what the paper did, its results for all six strategies (zero-shot, full fine-tuning, frozen lower layers, re-initialised top layers, adapters, LoRA), the authors' conclusions, our reading of its limits, and what it means for M3, M4 and Section A.
- Two atomic notes for the viva: `knowledge/catastrophic-forgetting.md` and `knowledge/lower-layers-learn-shared-sounds.md`.
- This plan and change file; generated indexes rebuilt.

## AI use in detail

- **What AI did (Claude Code):** downloaded the open-access PDF; drafted the source note and both atomic notes from the PDF and Joseph's summary; checked every number in the notes against the paper's Tables 2–6; drafted the issue comment.
- **What Joseph did himself:** read the paper and wrote the summary the note is built on ("fine-tuning is good for adapting large models to low-resource tasks, exploring several fine-tuning techniques"); reviewed and approved the issue comment.
- **How Joseph checked the AI's part:** read all three notes and confirmed they match his understanding of the paper. He did not re-check each number against the PDF himself; Claude's number check is the only one so far.

## Produced

- Learnings: none (no experiments)
- Decisions: none
- Results: none
