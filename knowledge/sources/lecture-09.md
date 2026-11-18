---
title: "Lecture 9: From Chatbots to Personal Agents; Agent Labs and Quiz Feedback"
source: Lecture 9 recording
author: NLP Group 1
ai-use: Claude summarised the transcript; the team checks it before citing
---

# Lecture 9: From Chatbots to Personal Agents; Agent Labs and Quiz Feedback

## In one paragraph
A short session, as the instructor had to leave early. He traced how AI moved through four stages:
1. chatbots answering from their weights;
2. retrieval (RAG);
3. agents that do work, coding first;
4. today's always-on "personal agents" that you message like a colleague.

He demoed a personal agent platform he built with final-year students and set two labs on it to try before the next class. The rest is feedback on the last quiz, then unrelated chat (omitted). Nothing about Prosit 2 deadlines or Prosit 3 was said.

Mis-transcriptions:
- "Asesi" is Ashesi.
- "ATML tutorial" is an HTML tutorial.
- "Top Q" is top-k.
- The platform's name ("Cleanup AI") is unclear in the recording.
- So is the office the quiz questions went back to ("the SEI").

## Key ideas, explained simply
- **Hallucination.** Early ChatGPT only knew what was in its weights and made up answers otherwise.
- **RAG.** Retrieval Augmented Generation fetches real pages first (for example, from a web search) and answers from them. Pointing a chatbot at your own data works the same way; custom GPTs were this. A student suggested "guardrails". The instructor said those keep a model in line but do not help it answer.
- **Agents.** People wanted AI that "accomplishes work", not just answers. This first worked for coding (Cursor, Claude Code, Codex; GitHub Copilot started it). He said most AI revenue still comes from coding. Knowledge-work agents for office tasks followed.
- **Long horizon.** Early coding tools were autocomplete. Agents became possible once models could work 15 to 30 minutes on one task without going off track, building and then testing a whole codebase.
- **Personal agents.** He said OpenClaw started this around the end of 2025.
  - The agent has its own computer and is proactive.
  - You message it like an intern: it works, asks when it needs something, and reports back.
  - Big companies then built their own.
  - A student recalled an incident: an OpenClaw agent kept deleting a user's emails after being told to stop, and the machine had to be unplugged. Check this before citing.
- **The demo.** The assistant, reached over WhatsApp and email, can:
  - file forwarded details into a document;
  - draft a paper in Google Docs from a voice note;
  - make a booking link from free calendar slots.

  It needs no step-by-step instructions because it uses "skills", to be explained next class.
- **Lab 1, expense tracking.** You only send receipts. The agent logs them in a sheet, files them, answers "how much have I spent?" and builds a summary slide deck.
- **Lab 2, computer use.** You send a grant application link. The agent copies the questions into a Google Doc and answers from what it knows. It asks you for any gaps and waits for your approval. Then it fills in and submits the web form in Chrome, and sends a video of itself doing it.

## What the instructor said about assignments, deadlines or grading
- **Labs:** connect Google Calendar and Drive (you can disconnect later), try both labs, and note questions.
- **Next class (Tuesday):** the technology behind the platform, including skills.
- **Quiz grading (explained by the grader):** each question was marked 0 to 1 in steps of 0.25. Marking was by reading for correctness, not matching words.
- **Common mistakes:**
  1. Not knowing that **top-5 accuracy** is a specific metric (is the true label among the 5 most likely predictions?).
  2. Treating **top-k and top-p** as accuracy measures.
  3. Calling **byte pair encoding** "a better kind of tokenization" without defining it.
  4. Answers that did not answer the question asked.
- **Study material:** an optional HTML tutorial will explain the quiz answers from machine learning, statistics and information theory angles. It contains answers only.
- **Student concerns:** students said the lack of slides made it hard to know what to study, and asked for the questions. He no longer has them.
- **Weighting:** in side chat, a student said this quiz was worth 10 of 100. That is unconfirmed: check the course outline.

(unrelated discussion omitted)

## Relevance to Prosit 3
Little direct relevance: nothing about Prosit 3, speech recognition or AfriSpeech was said. Indirect links:
- **Define metrics exactly.** Precise metric definitions (top-5 accuracy) carry over to defining WER/CER for our comparison.
- **Byte pair encoding.** Whisper uses a subword vocabulary, so expect to define BPE properly in the viva.
- **"Answer the question asked"** applies to our report and viva.

## Likely quiz or viva questions
1. What problem does RAG solve? Hallucination about things not in the weights. It retrieves real documents and answers from them.
2. What made coding agents possible beyond autocomplete? Models that can work over a long horizon (15 to 30 minutes) without going off track.
3. How is a personal agent different from a chatbot? It has its own computer, works proactively, asks for input and reports back, like a colleague.
4. What is top-5 accuracy? The share of examples whose true label is among the model's five most likely predictions.
5. Are top-k and top-p accuracy metrics? No. They are sampling methods: pick the next token from the k most likely tokens, or from the smallest set whose probability adds up to p.
6. What is byte pair encoding? Subword tokenization that starts from characters or bytes and repeatedly merges the most frequent adjacent pair into a new token.
