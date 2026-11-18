---
title: Chatbots do not learn from conversations: their weights are frozen, so memory is only the context
tags: [learning, lecture-03-part-1]
source: knowledge/sources/lecture-03-part-1.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Chatbots do not learn from conversations: their weights are frozen, so memory is only the context

After training, a chatbot's weights never change. What feels like "memory" is either the **context window** (the conversation so far) or saved prompts and facts fed back in. Every new session restarts from the same frozen model.

Changing that is the goal of two research ideas:
- **Continual learning** usually means fighting *catastrophic forgetting*: learning new things without losing old ones.
- **Lifelong learning** means always adding new knowledge, accepting some forgetting as long as you learn more than you forget. An agent should learn most from the problems it actually meets.

**Example:** tell a chatbot your name today; tomorrow, in a new session without saved facts, it does not know it, because nothing in its weights changed.

**For Prosit 3:** a deployed ASR model will not improve from doctors' corrections on its own. Improving it on Ayamra's terms means collecting corrected transcripts and fine-tuning again.

Related: [[evolutionary-strategies-vs-rl]], [[self-supervised-pretraining]]
