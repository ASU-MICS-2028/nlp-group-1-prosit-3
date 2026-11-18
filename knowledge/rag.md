---
title: RAG retrieves relevant documents at answer time and has the model answer from them
tags: [retrieval, lecture-04]
source: knowledge/sources/lecture-04.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# RAG retrieves relevant documents at answer time and has the model answer from them

Retrieval-Augmented Generation gives an LLM **external data** as a kind of external memory. The model already knows language; it lacks the specific facts in your PDF or database. A retriever finds the most relevant documents for the query, they are added to the prompt, and the model answers from them. This reduces hallucination "sometimes, to a large extent". Custom GPTs and chatbots over your own data work this way. Guardrails are different: they keep a model in line but do not help it answer.

**When not to use RAG:** retrieval adds latency. If the data is public, the model may already know it, so test that first. "RAG is not always the best answer."

**Example:** asked "How many leave days do I get?", the system retrieves the HR policy page and the model quotes it instead of guessing.

**For Prosit 3:** not core, but a clinical-term list retrieved per department could help correct drug names in transcripts.

Related: [[hallucination]], [[tf-idf]], [[sparse-vs-dense-retrieval]], [[ad-hoc-retrieval-vs-filtering]]
