---
title: Sparse retrieval matches word counts; dense retrieval matches meaning with embeddings
tags: [retrieval, lecture-04]
source: knowledge/sources/lecture-04.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Sparse retrieval matches word counts; dense retrieval matches meaning with embeddings

- **Sparse retrieval** represents documents by word counts, so most entries are zero. TF-IDF is the classic method and BM25 is "relatively newer". It matches exact words.
- **Dense retrieval** represents queries and documents with embeddings, short vectors where every number carries some meaning. It can match "physician" with "doctor" even with no shared word.

Lecture 4 taught only sparse retrieval but said projects would "most likely" use dense. BM25's formula was not given in class. Standard idea (source: lecture-04.md; Jurafsky and Martin, ch. 14): BM25 is TF-IDF with term frequency that saturates (the 10th mention adds little) and a correction for document length.

**Example:** the query "heart attack" finds a note saying "myocardial infarction" with dense retrieval, but not with plain TF-IDF.

**For Prosit 3:** not core; background for [[rag]].

Related: [[tf-idf]], [[word-embeddings]], [[rag]]
