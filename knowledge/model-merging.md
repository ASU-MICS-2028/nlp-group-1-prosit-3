---
title: Model merging combines two fine-tuned models of the same architecture into one that does both tasks
tags: [training, lecture-03-part-1]
source: knowledge/sources/lecture-03-part-1.md
author: NLP Group 1
ai-use: Claude extracted this from the lecture summary; the team checks it before citing
---

# Model merging combines two fine-tuned models of the same architecture into one that does both tasks

Take two models with the same architecture, each fine-tuned for a different task, and combine their parameters into one model of the same size. A neural network is non-linear, so simply averaging the weights should not work, but the speaker said that with "some tricks" it does: the merged model handles both tasks, each slightly worse than its original.

If people keep fine-tuning from the newest merged model, the speaker found no limit to the gains. If everyone fine-tunes once from the same old model, gains level off fast.

**Example:** merge a model fine-tuned for translation with one fine-tuned for summarisation; the result does both, a little worse at each.

**For Prosit 3:** not needed for our comparison, but it is one way a hospital could combine a clinical-dictation model with a general-English one without serving two models.

Related: [[lora]], [[instruction-tuning]]
