---
title: Enterprises use AI models under licences, in their own cloud, or as open weights to protect their data
tags: [deployment, lecture-11]
source: knowledge/sources/lecture-11.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Enterprises use AI models under licences, in their own cloud, or as open weights to protect their data

US enterprises protect their data in four main ways:
- **Licensed proprietary models** under legal agreements that protect their data.
- **Cloud-hosted copies**, e.g. an OpenAI model run inside AWS, so data never goes to OpenAI.
- **Open-weight models**, increasingly, run on their own hardware.
- **Custom harnesses** on top, which the instructor called one of the main opportunities for students.

He added that large incumbents with little competition (MTN was the example) adopt AI slowly because there is little pressure to innovate; AI-first companies could win but need capital and must pass regulation.

**Example:** a bank wants a chatbot but cannot send customer data abroad, so it runs an open-weight model in its own data centre.

**For Prosit 3:** patient audio is sensitive. An open model like Whisper, fine-tuned and hosted by Ayamra, keeps recordings in-house, which a third-party speech API may not.

Related: [[model-plus-harness]], [[backend-between-page-and-agent]]
