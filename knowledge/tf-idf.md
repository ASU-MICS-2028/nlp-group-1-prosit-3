---
title: TF-IDF scores a word in a document by how often it appears there, damped by a log
tags: [retrieval, lecture-04]
source: knowledge/sources/lecture-04.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# TF-IDF scores a word in a document by how often it appears there, damped by a log

**Bag of words:** a document becomes word counts, with order ignored. Counts for every term in every document form a **term-document matrix**; a column is a document's vector, a row is a word's vector, so text can be compared with arithmetic.

**Term frequency (as given):** tf = 1 + log10(count) if count > 0, else 0. The log quietens very common words (like a banana taking over a smoothie) while keeping order; the guard avoids log(0), which is undefined. TF-IDF multiplies tf by **IDF** (inverse document frequency), which Lecture 4 left for reading. Standard definition (source: lecture-04.md; Jurafsky and Martin, ch. 6): idf = log10(N / df), where df is the number of documents containing the term, so words in every document score near 0. Scores go in an **inverted index**, and the query is ranked against documents by cosine similarity.

**Worked numbers:** "battle" appears 13 times in Henry V: tf = 1 + log10(13) ≈ 2.11. A count of 1,000 gives only 4.

**For Prosit 3:** not core; TF-IDF is the classic sparse method behind [[rag]].

Related: [[sparse-vs-dense-retrieval]], [[rag]], [[ad-hoc-retrieval-vs-filtering]]
