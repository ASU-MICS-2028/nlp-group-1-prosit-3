---
title: "Liu et al. 2024: fine-tuning makes Whisper good at low-resource languages, and which fine-tuning strategy to pick"
source: "Yunpeng Liu, Xukui Yang and Dan Qu. 2024. Exploration of Whisper fine-tuning strategies for low-resource ASR. EURASIP Journal on Audio, Speech, and Music Processing, 2024(1):29. doi:10.1186/s13636-024-00349-3 (open access, CC BY 4.0)"
author: Joseph Etse
ai-use: Joseph read the paper and wrote the one-line summary; Claude drafted the note from the PDF and Joseph's summary, and checked every number against the paper's tables; Joseph reviews
---

# Liu et al. 2024: Whisper fine-tuning strategies for low-resource ASR

## In one paragraph
Fine-tuning is a good way to adapt a large pre-trained speech model to a low-resource language, and the paper compares several ways of doing it. It asks three questions:
1. How much can fine-tuning improve Whisper?
2. Which part of the model matters most when fine-tuning?
3. What do parameter-efficient methods gain and lose?

The authors fine-tune **Whisper-large-v2** (1.15B parameters) on seven low-resource languages from the FLEURS dataset: Afrikaans, Belarusian, Icelandic, Kazakh, Marathi, Nepali and Swahili. Each has 3–17 hours of speech in total, and under 10 hours for training. Every strategy they tried helped a lot. Full fine-tuning helped most per experiment; freezing the lowest encoder layers helped slightly more; adapters and LoRA were nearly as good at a fraction of the cost.

## Setup
- **Data:** FLEURS, about 12 hours per language, with different speakers in train and test. Swahili had 16.2 hours in total (3,070 training clips). Afrikaans had 5.2 hours.
- **Model:** Whisper-large-v2. They skipped large-v3 because its larger training set no longer makes these languages "low-resource".
- **Training:**
  - Following the Hugging Face fine-tuning example: AdamW, a learning rate of 1e-5 with 10% warm-up then a linear decay, 35 epochs, batch size 8, on one A40 GPU.
  - A checkpoint every 200 steps; the one with the lowest test WER was kept.
- **Metric:** word error rate (WER).

## Results (average WER over the seven languages; from Tables 4–6)

| Strategy | What is trained | Avg WER | Swahili | Training time |
|---|---|---|---|---|
| Zero-shot (no fine-tuning) | nothing | 40.39% | 39.3% | none |
| **Full ("vanilla") fine-tuning** | all 1.15B weights | **17.39%** | 15.62% | 14.6 h |
| Freeze the bottom encoder layers | everything above layer *n* (best *n* = 10–20 of 32) | **16.30%** (best) | 14.70% | less than full |
| Re-initialise the top encoder layer(s) | top layers reset, then trained | 20.82% | 19.85% | n/a |
| Bottleneck adapters | small modules added after every layer, 9.2M params (≈0.8%) | 19.02% | 16.69% | 2.8 h |
| LoRA (rank 32, alpha 64, on query and value) | 7.7M params (≈0.67%) | 21.40% | 18.97% | 2.6 h |

- **Full fine-tuning cut WER by 57% (relative)** with under 20 hours of data per language.
- **Freezing the lower layers** gave a further 6% relative gain. Their layer-by-layer analysis (CKA similarity before and after fine-tuning) shows why:
  - the bottom ~15 encoder layers barely change, because they encode sounds shared across languages;
  - only the top layers, which encode language-specific features, need to move.
- **Re-initialising top layers made things worse.** Resetting even one layer hurt, and resetting five lost the ability to recognise speech entirely. The pre-trained weights are already a good starting point.
- **Adapters and LoRA** were 1.6 and 4.0 points worse than full fine-tuning, but trained 5.2 and 5.6 times faster. Because the original weights stay frozen, they also avoid catastrophic forgetting. Adapters in only the top 6–10 encoder layers did about as well as adapters everywhere (18.65%).
- **Size matters before fine-tuning too** (Table 3, OpenAI's zero-shot numbers): average WER is 109.5% for Tiny, 96.1% for Base, 68.9% for Small and 40.4% for large-v2.

## The authors' conclusions
- All five strategies improve Whisper on low-resource languages. Pick one based on your accuracy needs and your compute.
- If accuracy matters most, use full fine-tuning, ideally with the lower encoder layers frozen.
- If compute, time, or keeping the model's other abilities matters, use adapters or LoRA. Adapters are their next research focus.
- Fine-tuning on several similar languages together is a promising next step.

## Limits (ours, reading it)
- **Unreliable checkpoint choice:** they picked the best checkpoint by *test* WER, which flatters every number a little. We pick ours on dev clips.
- **No repeats:** one run per setting, with no variance reported.
- **One model:** only large-v2. They expect the conclusions to transfer to smaller models but don't test it.
- **Different task:** other languages, not accented English, and no medical vocabulary.

## What it means for us
- **M3 (full fine-tune):** our result matches theirs. Whisper-small on AfriSpeech went from 0.350 to 0.156 WER, a **55%** relative cut against their 57%. We used the same recipe family (AdamW, 1e-5, warm-up, linear decay).
- **M4 (LoRA, Eric):** expect LoRA to land a little worse than full fine-tuning, but far cheaper. Their gap was 4 points. If M4 is close to 0.156, LoRA is the practical choice for Ayamra.
- **A cheap thing to try:** freezing the lower encoder layers of whisper-small might gain a little and train faster. Optional, only if GPU time allows.
- **Section A:** this is the main evidence that a pre-trained transformer adapts with hours, not thousands of hours, of speech, unlike an RNN trained from scratch.

Related: [[catastrophic-forgetting]], [[lower-layers-learn-shared-sounds]], [[lora]], [[peft]], [[encoder-decoder]], [[data-size-decides-which-model-wins]]
