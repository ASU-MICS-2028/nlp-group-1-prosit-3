---
title: Fine-tuning every weight can make a model forget what it could do before
tags: [fine-tuning, M3, M4]
source: knowledge/sources/liu-2024-whisper-fine-tuning.md
author: Joseph Etse
ai-use: Claude drafted from the paper; Joseph reviewed
---

# Fine-tuning every weight can make a model forget what it could do before

When you fine-tune all of a model's weights on one task or language, it gets better at that task but can lose abilities it had before, such as other languages or translation. This is **catastrophic forgetting**.

It is different from overfitting:
- **Overfitting** is doing worse on new data of the *same* task.
- **Forgetting** is doing worse on *other* tasks.

**How to avoid it:** freeze the original weights and train only small added parts, such as adapters or [[lora]]. The original model is untouched, so nothing is forgotten. You can even keep one adapter per task.

**Example:** our fully fine-tuned whisper-small writes AfriSpeech-style English well. It may have become worse at, say, French or translation, which we did not test. A hospital that only needs English dictation does not mind. A product serving many languages from one model would.

Related: [[peft]], [[liu-2024-whisper-fine-tuning]]
