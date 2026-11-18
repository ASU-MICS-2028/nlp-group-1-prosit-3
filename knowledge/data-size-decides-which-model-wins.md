---
title: Simpler models can win on small data; bigger models win once there is enough
tags: [modelling, prosit-1]
source: knowledge/sources/prosit-1.md
author: Joseph Etse
ai-use: Claude drafted from the source; Joseph reviewed
---

# Simpler models can win on small data; bigger models win once there is enough

In Prosit 1, n-gram models beat neural models below about 10,000 training sentences, and neural models (an LSTM, a small Transformer) won above that. The best was an LSTM at perplexity 46 on 100k sentences.

**For Prosit 3:** compare models at more than one training-data size, not just one, so the report can say *when* an RNN is good enough and when pre-trained transformers pay off. A scaling curve like this is the kind of evidence that earned credit in Prosit 1.

Related: [[rnn]], [[measure-before-adding-complexity]]
