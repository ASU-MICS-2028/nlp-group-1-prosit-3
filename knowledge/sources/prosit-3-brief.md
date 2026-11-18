---
title: The Prosit 3 brief - Ayamra hospital dictation (supervised speech recognition with transformers)
source: Grad NLP Prosit 3 brief (PDF on Canvas) and Lecture 12 (2026-11-09)
author: NLP Group 1
ai-use: Claude summarised the brief; the wording of the four questions and the deliverables is copied from it
---

# The Prosit 3 brief

**Title:** "PROSIT 3: Supervised Speech Recognition with Transformers" (ICS554, Fall 2026).

## The scenario

Ayamra is a network of hospitals in many major African cities. Doctors spend too long writing notes, and speaking is faster than writing, so Ayamra wants doctors to dictate notes and have them transcribed. A consultant told them to use a **recurrent neural network (RNN)** and the open **AfriSpeech-200** dataset (https://huggingface.co/datasets/intronhealth/afrispeech-200). We were hired as their AI technologists.

## The four questions

1. What are recurrent neural networks (RNNs)? How can they be used to solve the problem?
2. Are RNNs the best approach to solving this problem? What are their advantages and disadvantages versus other approaches when it comes to solving this problem?
3. Would you recommend that they build their speech-to-text system with RNNs? If not, what would be your recommendation and why?
4. Could you follow your recommendation to build a speech-to-text system that solves their problem?

The instructor's hint (Lecture 12): "don't blindly say yes"; either answer needs a reason. The whole team must recommend the same approach, because we build it together.

## Deliverables

| What | Details |
|---|---|
| Technical report | A convincing **scholarly** case for RNNs or our alternative, plus how we built it: approach, implementation, evaluation. ACL-style format, **under 10 pages**, GitHub link on page 1. See [[report-format]] |
| Presentation | 10 minutes, a team presentation that summarises the report in an engaging way. GitHub link on slide 1; uploaded to Canvas |
| Code | On GitHub (this repo) |

## Grading

- Group presentation: **20%** (how educational it was; how well they understand what the group and each member did)
- Technical report: **45%**
  - Section A: 20%
  - Section B: 25% (implementation and results 20%, writing quality 5%)
- Viva quiz: **35%**

Joint vs individual report, and what counts toward the page limit, are still pending (decision 0006).

## Learning outcomes named in the brief

- Construct, train, evaluate and deploy speech recognition systems, focusing on scalability, robustness and adaptability to low-resource African languages.
- Critically read, interpret and implement NLP research papers as reproducible experiments.
- Explain NLP concepts clearly to technical and non-technical audiences.
- Propose, implement and evaluate novel ideas for contextually relevant NLP for Africa.

## Readings

Jurafsky and Martin, chapters 15–17, mostly 16 (Lecture 12). From the course outline: Liu et al. 2024 (Whisper fine-tuning for low-resource ASR), Sharma et al. 2025 (Whisper Tiny for Swahili), Ghimire et al. 2024 (PEFT for low-resource ASR).
