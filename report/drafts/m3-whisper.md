---
title: "Section B draft: M3, Whisper zero-shot and full fine-tune"
owner: Joseph Etse
issue: "#6"
status: draft for Joseph's review
ai-use: Claude drafted the text, table and slide plan from the committed run records; Joseph reviews, rewrites in his own words and checks every number against eval/results/
---

# Section B draft: M3, Whisper zero-shot and full fine-tune

Every number below comes from a committed run record: `eval/results/m3-*/run.md`, `scores.json` and `failure-checks.csv`. All runs are finished; nothing is pending.

---

## B.x Whisper: zero-shot and full fine-tuning

**Model and setup.** Whisper is an encoder-decoder transformer trained on 680,000 hours of weakly labelled web audio (Radford et al., 2023). We test it in two ways on our fixed test set: 1,000 AfriSpeech-200 clips, half clinical and half general, from 104 accents (Olatunji et al., 2023).
- **Zero-shot:** the released weights, unchanged.
- **Fully fine-tuned:** every weight updated on the AfriSpeech train split.

All runs force English output. They use Whisper's temperature fallback, which re-decodes a clip at a higher temperature when the output is too repetitive (gzip compression ratio above 1.35). Without the fallback, whisper-small reached WER 0.480, because 49 clips fell into repetition loops such as "i do i do i do". With it, WER was 0.350.

**Fine-tuning.**
- **Data:** the full train split, 57,819 clips. Clips longer than 30 s, Whisper's input window, are skipped.
- **Schedule:** 4,000 steps at an effective batch of 16 (8 × 2 gradient accumulation). AdamW at a learning rate of 1e-5, with 500 warm-up steps and a linear decay.
- **Precision:** fp16 mixed precision, with gradient clipping at 1.0.
- **Checkpoint choice:** we kept the checkpoint with the lowest WER on 200 dev clips, checked every 500 steps.
- **Cost:** the run took 2.8 hours on one free Kaggle T4 GPU (16 GB), at no cost.

**Results.** Table 1 compares the models.

| Model | Params | WER | CER | Clinical WER | General WER |
|---|---|---|---|---|---|
| whisper-tiny, zero-shot | 39M | 0.571 | 0.322 | 0.629 | 0.528 |
| whisper-base, zero-shot | 74M | 0.464 | 0.268 | 0.520 | 0.423 |
| whisper-small, zero-shot | 244M | 0.350 | 0.204 | 0.389 | 0.322 |
| whisper-small, zero-shot, language detected | 244M | 0.464 | 0.297 | 0.516 | 0.426 |
| whisper-large-v3-turbo, zero-shot | 809M | 0.293 | 0.174 | 0.345 | 0.255 |
| **whisper-small, fine-tuned (4k steps)** | 244M | **0.156** | **0.071** | **0.200** | **0.123** |
| whisper-small, fine-tuned (8k steps) | 244M | 0.152 | 0.070 | 0.194 | 0.121 |

*Table 1: Word and character error rates on the 1,000-clip test set. Every run uses temperature fallback and, unless stated otherwise, forced English.*

**What size buys, and what training buys.**
- **Size:** without training, a larger model helps, but each step helps less. Tiny to base gains 10.7 points and base to small 11.4, but turbo, with 3.3 times the parameters of small, gains only 5.7.
- **Training:** fine-tuning small on AfriSpeech gains 19.4 points, cutting its error by more than half. It ends 13.7 points below turbo.
- **By accent:** every accent with at least 30 test clips improved. Swahili fell from 0.269 to 0.111, and Igbo, the hardest, from 0.404 to 0.158.

**What fine-tuning fixed.** Two errors dominated zero-shot output (Table 2).
- **Repetition loops:** clips with WER above 1 fell from 45 to 10.
- **Dictated punctuation:** dictating doctors say "comma" and "full stop", and AfriSpeech's references don't write them as words. Zero-shot Whisper wrote them as words in 347 clips. After fine-tuning, only 12 clips still did.

These are style errors, not hearing errors. A small amount of in-domain training removes them, but model size does not. Bigger models loop less, but they write the punctuation words in more clips (224 for tiny, 383 for turbo), because they copy the dictation more faithfully.

| Model | Clips with WER > 1 | Clips with spoken punctuation not in the reference |
|---|---|---|
| whisper-tiny, zero-shot | 123 | 224 |
| whisper-base, zero-shot | 77 | 254 |
| whisper-small, zero-shot | 45 | 347 |
| whisper-large-v3-turbo, zero-shot | 35 | 383 |
| whisper-small, fine-tuned | 10 | 12 |

*Table 2: The two main zero-shot failures before and after fine-tuning (`models/whisper_full/failure_checks.py`).*

**What remains.**
- **Clinical speech is still the hardest.** Its WER is 0.200 against 0.123 for general speech: drug names, doses and medical terms. The error analysis (Section B.y) breaks this down.
- **Training had not converged.** Dev WER was still falling at step 4,000 (0.164 → 0.161). Training for 8,000 steps instead (5.6 GPU hours) brought test WER only to 0.152, a gain of 0.4 points for double the cost and within what one seed can show. Most of the gain comes in the first 4,000 steps.
- **Limits:** these are single runs with one seed. The dev check used only 200 clips.

**Language detection.** Forcing English matters. When whisper-small detected the language itself, WER rose from 0.350 to 0.464: it took some accented English for another language and wrote 66 clips in other scripts, such as Arabic, Bengali and Georgian, and loops rose from 45 to 75 clips. Every AfriSpeech clip is English, so all our runs force it.

---

## Slide segment (about 1 minute, one slide plus one build)

**Title:** *Teach the listener our clinic: fine-tuned Whisper halves the errors*

**Story hook:** a new nurse transferred from abroad is skilled, but on day one mishears local names and writes "comma" when the doctor says it. After a few weeks on the ward, she stops. Zero-shot Whisper is that nurse on day one. The fine-tuned model is the same nurse after training on our ward's recordings.

**On the slide:**
1. A bar chart of WER: tiny 0.571, base 0.464, small 0.350, turbo 0.293 (all zero-shot), then small fine-tuned **0.156**.
2. Build: two before → after counts.
   - "Repetition loops: 45 → 10"
   - "'Comma' / 'full stop' written as words: 347 → 12"
3. A footer line: "2.8 GPU hours on a free Kaggle T4. Cost: 0 USD."

**Speaker notes:** "A three-times bigger Whisper helps a little. Training a small one on our recordings helps three times more, and it costs nothing. The errors it still makes are clinical words, which Michael's analysis shows next."

**Open question for the team:** which analogy does the whole deck use? This one, a nurse learning the ward, only works if the other segments fit it too.
