---
title: An agent needs tools because an LLM only produces text; MCP lets services list their tools
tags: [agents, lecture-08]
source: knowledge/sources/lecture-08.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# An agent needs tools because an LLM only produces text; MCP lets services list their tools

An LLM can *say* "write this code to a file" or "start a server", but it cannot do either. The agent needs a **tool** for each action: writing files, running code, setting up a database. The model decides which tool to call; the tool does it and returns the result.

**MCP (Model Context Protocol)** is a standard way for a service to list its tools so an agent can discover and call them, instead of a human reading documentation to find the right API calls.

**Example (Lecture 8):** setting up a Supabase database takes many API calls (create database, create tables, set privileges). An MCP server for the service lists those as tools for the agent. Supabase was only an example.

**For Prosit 3:** if Ayamra later wanted an assistant that files transcripts into records, the ASR model would be one tool the agent calls.

Related: [[agent-loop]], [[model-plus-harness]], [[backend-between-page-and-agent]]
