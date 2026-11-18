---
title: "Lecture 10: Harness Engineering, Choosing Models with Evals; Prosit 2 Wrap-up and the Viva"
source: Lecture 10 recording
author: NLP Group 1
ai-use: Claude summarised the transcript; the team checks it before citing
---

# Lecture 10: Harness Engineering, Choosing Models with Evals; Prosit 2 Wrap-up and the Viva

## In one paragraph
The instructor's main point was that an agent is a model plus a harness, and that much of today's value in AI comes from building good harnesses, not from training models. He covered choosing models with evals, and how a good harness can lift a weaker model. Two groups gave Prosit 2 updates, then a long discussion covered workload and the rule that everyone must understand the whole project. Schedule: Prosit 2 due by the weekend, Tuesday for starting Prosit 3, the viva code quiz the week after. Speaker labels are mixed up, so who said what is not always clear.

Mis-transcriptions:
- "process three", "proceed period" and "prosecute" are Prosit 3, the Prosit period and Prosit 2.
- "Thermis" is probably Hermes (named in Lecture 8), and "Rekli" is probably Replit.
- "Kessel" is a coding agent whose name is unclear. Do not cite the claim that it was bought for $60 billion.
- "Lengora", "Robots", "MUSE", "Duality" and "environmentals" (possibly n-gram models) are unclear in the recording.

## Key ideas, explained simply
- **Agent = model + harness.** In his analogy, the model is the car's engine (the intelligence) and the harness is the car body. The harness holds the tools that act: writing files, running code in a sandbox, setting up a database.
- **The agent loop:** ask the model "what next?", take the step, send back the result, repeat until done.
- **Three ways to be "in AI":** train models (few can afford it), fine-tune open models, or build harnesses, where he said most value is now created.
- **Claude Code is a harness, not a model.** The model only predicts tokens; Claude Code (like Codex) is a harness bundled with it.
- **Vertical harnesses:** each field needs its own tools (accounting needs a law-lookup tool). Prosit 2 is a coding harness; Gamma is a slides harness.
- **Choosing a model: evals.** An eval is a set of prompts with a definition of what a good output looks like. You run each candidate model on it and compare, and you rerun it when a new model comes out. He said Gamma reportedly makes about 200 LLM calls across 30 to 40 models per deck, picking the best or cheapest for each subtask, plus a vision-model check of the layout.
- **A good harness can lift a weaker model.** In his illustration, a strong model alone gets code right 85% of the time. A weaker one gets it right 70% of the time, but its harness runs the code in a sandbox and sends errors back for a retry, so it can reach about 95%.
- **Cost:** later, an eval answers "can a $5 model do this $10 job?"
- **A group's eval:** a student reported trying Opus 5.5, Sonnet 5.5 and Haiku. Opus scored about 96% and Haiku was lowest, in the 80s. The instructor agreed this is essentially an eval.

## What the instructor said about assignments, deadlines or grading
- **Prosit 2 deadline:** submit by Friday, at the latest Sunday.
- **Run end to end, every team.** A user must be able to open the page, say what to build and get a deployed API to test, even a simple one. "You may underestimate what you need to do to bring everything together."
- **Group updates:** one group was nearly done (a hosted front end that deploys a backend on request). The other runs its agents in sequence: requirements, orchestrator, code agent with a sandbox, test agent.
- **Know 100% of the project.** He called this non-negotiable. Each student should be able to do the whole task alone; group work helps you learn it but does not split you into specialists. "AI has finished the project, but you haven't."
- **Code:**
  - Remove extraneous files left behind by AI.
  - Code must be readable to you: "Code cannot be a strange language to you as a computer scientist, at least not in 2026."
- **The viva:**
  - Results were about half decent and half concerning, because some students did not understand the code their group submitted.
  - The format will not change.
- **Workload:** expect 50 to 60 hours a week.
- **Schedule:**
  - The instructor flies out on Monday and teaches remotely until the end of the semester. He will not teach next semester.
  - Tuesday's class is for Prosit 3 work.
  - The viva code quiz is the following week (Tuesday or Thursday; unclear in the recording). Another quiz, heard as "section E", is unclear.
- **Final project:** students choose the topic within NLP. It need not use a language model.

(unrelated discussion omitted)

## Relevance to Prosit 3
- **Evals for model choice: directly relevant.** Comparing BiLSTM+CTC, wav2vec2, Whisper full fine-tune and Whisper+LoRA is an eval. It needs:
  - a fixed AfriSpeech-200 test set;
  - a defined "good" (WER/CER, ideally on clinical terms);
  - every model scored on the same set.
  "Can a cheaper model do it?" matches our compute trade-off.
- **Harness engineering: little direct relevance.** Prosit 3 trains and fine-tunes models rather than wrapping them in a harness.
- **Timing:** Prosit 3 work starts in Tuesday's class.
- **Viva:** every member must understand all four models and the whole pipeline.
- **Speech recognition:** nothing technical was said. The instructor only mentioned past speech recognition research of his own.

## Likely quiz or viva questions
1. What is the difference between a model and a harness? The model predicts tokens. The harness provides the tools and the loop that act on its output.
2. Is Claude Code a model? No. It is a harness, bundled with the Claude model.
3. What is an eval? A set of prompts with a definition of a good output, used to score and compare candidate models.
4. How can a weaker model beat a stronger one? Its harness tests the output and sends errors back for a retry (70% to about 95% in his example).
