---
title: "Section A draft: the scholarly case (RNNs vs alternatives, recommendation)"
owner: Joseph Etse
issue: "#12"
status: draft for Joseph's review
ai-use: Claude drafted the argument and literature review. The three course readings (Liu et al., 2024; Ghimire et al., 2024; Sharma et al., 2025) were read in full and every number from them was checked against the PDFs. Our own numbers come from eval/results/m3-*. Joseph reviews, rewrites in his own words, and checks the references marked "check" below.
---

# Section A draft: the scholarly case

**Before this is final:**
- **[M1] [M2] [M4]** mark the numbers still to come from Bernard (RNN), Alice (wav2vec2) and Eric (LoRA), on the same 1,000-clip test set.
- **The recommendation in A.3 is the M3 evidence so far.** The team must agree it as a decision record before anyone submits ([[team-agrees-on-one-recommendation]]).
- **Joint or individual is still unconfirmed** (decision 0006). If the report is individual, this is Joseph's own Section A; if joint, it is split by topic.
- **Length:** about 1,650 words, or about 2.5 ACL pages with the table and references. Trim A.2.2 first if the page limit bites.

---

## A.1 What recurrent neural networks are, and how they would solve Ayamra's problem

Ayamra's task is automatic speech recognition (ASR): a doctor's recorded voice goes in, and the written note comes out. Speech is a sequence. A 10-second dictation becomes about 1,000 frames of a mel spectrogram, one every 10 ms, and the meaning of each sound depends on the sounds around it.

**The basic idea.** A recurrent neural network (RNN) reads a sequence one step at a time. At each step it combines the current input with a hidden state that summarises everything read so far, using the same weights at every step, so it can handle a clip of any length. Plain RNNs forget over long spans, because the training signal shrinks as it is passed back through many steps. The long short-term memory (LSTM) adds gates that decide what to keep and what to forget, which lets information last across hundreds of frames (Hochreiter and Schmidhuber, 1997). A bidirectional LSTM (BiLSTM) runs one LSTM forwards and one backwards, so each frame sees both what came before and what comes after. That suits dictation, where the whole recording exists before it is transcribed.

**The alignment problem.** A recording has far more frames than its transcript has letters, and no one marks which frame belongs to which letter. Connectionist temporal classification (CTC) solves this (Graves et al., 2006):
- the network outputs, at every frame, a probability for each character plus a special "blank";
- training adds up the probability of every frame-by-frame path that collapses to the correct transcript;
- decoding merges repeated characters and drops the blanks.

Graves et al. (2013) showed that deep bidirectional LSTMs trained this way could recognise speech accurately without hand-built pronunciation models. Attention-based encoder-decoders with RNN encoders and decoders followed (Chan et al., 2016).

**For Ayamra,** the consultant's design would be:
1. turn each dictation into an 80-band log-mel spectrogram;
2. pass it through a stack of BiLSTM layers;
3. train the network on AfriSpeech-200 (Olatunji et al., 2023) with the CTC loss, so it outputs characters directly.

AfriSpeech-200 fits the problem. It has about 200 hours of African-accented English, read by 2,463 speakers with about 120 accents, and most of its clips are clinical sentences. The training split holds 173 hours. Our M1 model builds exactly this design (Section B.1).

## A.2 Are RNNs the best approach? Strengths and weaknesses against the alternatives

### A.2.1 The alternatives

Two shifts since the RNN era change the answer.

**Transformers replaced recurrence with attention.** A transformer lets every frame attend directly to every other frame, so it has no step-by-step chain to forget along, and all frames are processed in parallel on a GPU (Vaswani et al., 2017). Speech models soon adopted it, often with convolution added for local acoustic detail (Gulati et al., 2020).

**Pre-training made labelled data go further.** Two families matter for us:
- **wav2vec 2.0** learns speech representations from unlabelled audio alone, then needs only a little transcribed speech and a CTC layer to become a recogniser (Baevski et al., 2020).
- **Whisper** is a transformer encoder-decoder trained on 680,000 hours of weakly labelled audio from the web, in many languages (Radford et al., 2023). It transcribes out of the box ("zero-shot") and can be fine-tuned further.

These models arrive already knowing how speech sounds and how English is written. An RNN trained from scratch must learn all of that from Ayamra's data.

### A.2.2 What the low-resource literature shows

The three course readings all test whether fine-tuning a pre-trained Whisper is enough when target-language data is scarce. Each finds that it is.

**Liu, Yang and Qu (2024)** compared five fine-tuning strategies for Whisper-large-v2 on seven low-resource languages from FLEURS, including Afrikaans and Swahili, each with under 10 hours of training speech.
- **Full ("vanilla") fine-tuning** cut the average word error rate (WER) from 40.39% to 17.39%, a 57% relative reduction. Swahili fell from 39.3% to 15.6%.
- **Freezing the bottom 10–20 encoder layers** did slightly better, at 16.30%. Their layer analysis showed that the lower layers encode sounds shared across languages, and only the top layers need to change.
- **Parameter-efficient methods trained under 1% of the weights.** Bottleneck adapters reached 19.02%, and LoRA (Hu et al., 2022) reached 21.40%, while training 5.2 and 5.6 times faster. They also avoid "catastrophic forgetting" of the model's other abilities.
- **Model size matters on its own as well.** In the zero-shot results they report (their Table 3), the smallest Whisper models are far behind the larger ones on these languages: an average WER of 109.5% for Tiny and 68.9% for Small.

**Ghimire, Poudyal and Bal (2024)** fine-tuned Whisper-large-v2 on just 4 hours of Nepali.
- Zero-shot, its output drifted towards Hindi, at a WER of 47.1%.
- Full fine-tuning brought it to 36.2%.
- Three LoRA adapters, trained in stages and then merged, brought it to 27.9%.
- That beat the HMM (29.45%) and CNN-GRU (37.50%) systems published for Nepali, although those were measured on other test sets.

**Sharma, Pandya and Shukla (2025)** fine-tuned the smallest Whisper, Tiny (39M parameters), on 19.7 hours of Swahili.
- WER fell from 82.95% after 5 epochs to 30.62% after 100 epochs.
- The remaining errors were phonetic near-misses, names, and repetition loops on hard audio.
- They conclude that Tiny lacks the capacity for practical use. They recommend Base as the minimum and Small as "the optimal balance of performance and efficiency".

**Three lessons for Ayamra:**
1. A pre-trained transformer adapts well with far less data than AfriSpeech's 173 hours.
2. How much it improves depends on model size.
3. The same failures, wrong-language output and repetition loops, appear across studies, and fine-tuning reduces them.

Our own measurements on AfriSpeech-200 repeat all three (Section B.3).
- **Fine-tuning helps:** fully fine-tuning Whisper-small for 2.8 GPU hours cut test WER from 0.350 to 0.156. That is a 55% relative reduction, close to Liu et al.'s 57%.
- **Size helps:** zero-shot WER falls from 0.571 for Tiny to 0.293 for large-v3-turbo.
- **The same failures appear:** letting Whisper detect the language itself raised WER to 0.464, as accented English was taken for other languages. Fine-tuning cut repetition loops from 45 clips to 10.

### A.2.3 Strengths and weaknesses for this problem

Table A1 weighs a BiLSTM-CTC trained from scratch against the pre-trained alternatives, on what matters to Ayamra.

| Criterion | BiLSTM + CTC from scratch (M1) | wav2vec 2.0 + CTC (M2) | Whisper fine-tuned (M3, M4) |
|---|---|---|---|
| Accuracy on our test set (WER) | [M1] | [M2] | 0.156 full fine-tune; [M4] LoRA |
| Knowledge before seeing our data | None: learns sounds, spelling and accents from 173 h | Sounds, from unlabelled audio | Sounds, language and spelling, from 680,000 h |
| Clinical vocabulary | Learned only from training sentences; CTC has no built-in language model, so rare drug names are misspelled | Same CTC limitation | The decoder is a language model, which helps with spelling; clinical WER is still 0.200 vs 0.123 for general speech |
| Training cost | Small model, but recurrence is sequential, so it is slow per hour of audio | Moderate | 2.8 h on one free GPU (full fine-tune); LoRA cheaper still |
| Running cost | Lowest: small, CPU-friendly | Moderate | Higher (244M parameters), but runs on one GPU |
| Live, word-by-word streaming | Possible with a one-directional LSTM | Possible | Not designed for it: works on 30 s windows |
| Known failure modes | Weak long-range context, spelling errors | Spelling errors | Repetition loops, wrong-language output, dictated punctuation written as words; all reduced by fine-tuning and forcing English |

*Table A1: How the approaches compare for Ayamra's dictation task.*

**Where an RNN would still win:** a cheap, on-device recogniser for a small, fixed vocabulary, or live streaming on weak hardware. Ayamra's need is different:
- the vocabulary is open, and clinical;
- doctors finish a dictation before it is transcribed, so streaming is not required;
- the hardware can be shared hospital servers.

The RNN's advantages do not address Ayamra's hardest problems, which are accents and medical words, and its main weakness does: it starts with no knowledge of speech or English.

## A.3 Our recommendation

We would not build Ayamra's system as an RNN trained from scratch. We recommend fine-tuning a pre-trained transformer, Whisper-small, on AfriSpeech-200, with English output forced. [Final wording after the team agrees; update if M2 or M4 beats M3.]

**Why:**
1. **Accuracy.** On the same 1,000 test clips, fine-tuned Whisper-small reaches a WER of 0.156, against [M1] for the BiLSTM-CTC baseline. It also beats every zero-shot model, including one 3.3 times larger (0.293).
2. **Data efficiency.** The literature (Liu et al., 2024; Ghimire et al., 2024) and our results agree: a pre-trained model needs hours, not thousands of hours, of in-domain speech to adapt. AfriSpeech's 173 hours are more than enough to fine-tune, but little for learning speech from nothing.
3. **Cost.** Fine-tuning took 2.8 hours on a free Kaggle GPU. Doubling it to 8,000 steps gained only 0.4 points, so Ayamra would not need large compute. LoRA can cut training cost further [M4].
4. **Choice of size.** Small is the smallest Whisper we would deploy. Tiny and Base lag well behind at zero-shot (0.571 and 0.464), which agrees with Sharma et al. (2025).

**What remains** for Ayamra before clinical use:
- **Clinical words are still the hardest** (WER 0.200 vs 0.123). A doctor should review each note before it enters the record, and Section B.y analyses these errors.
- **A real hospital is noisier** than AfriSpeech's read speech. The system should be tested on recordings from the wards themselves.
- **Licence.** AfriSpeech-200 is licensed for non-commercial use only, so a production system needs Ayamra's own recordings, or a licence agreement, before deployment.

---

## References

Checked against the paper: Liu et al. (2024), Ghimire et al. (2024), Sharma et al. (2025), Radford et al. (2023). Marked **(check)**: add the DOI or ACL Anthology link and confirm the details before submitting.

- Alexei Baevski, Yuhao Zhou, Abdelrahman Mohamed, and Michael Auli. 2020. wav2vec 2.0: A framework for self-supervised learning of speech representations. In *Advances in Neural Information Processing Systems 33*. **(check)**
- William Chan, Navdeep Jaitly, Quoc Le, and Oriol Vinyals. 2016. Listen, attend and spell: A neural network for large vocabulary conversational speech recognition. In *Proceedings of ICASSP 2016*, pages 4960–4964. doi:10.1109/ICASSP.2016.7472621.
- Rupak Raj Ghimire, Prakash Poudyal, and Bal Krishna Bal. 2024. Improving on the limitations of the ASR model in low-resourced environments using parameter-efficient fine-tuning. In *Proceedings of the 21st International Conference on Natural Language Processing (ICON)*, pages 408–415. https://aclanthology.org/2024.icon-1.47/
- Alex Graves, Santiago Fernández, Faustino Gomez, and Jürgen Schmidhuber. 2006. Connectionist temporal classification: Labelling unsegmented sequence data with recurrent neural networks. In *Proceedings of ICML 2006*. **(check)**
- Alex Graves, Abdel-rahman Mohamed, and Geoffrey Hinton. 2013. Speech recognition with deep recurrent neural networks. In *Proceedings of ICASSP 2013*, pages 6645–6649. doi:10.1109/ICASSP.2013.6638947.
- Anmol Gulati et al. 2020. Conformer: Convolution-augmented transformer for speech recognition. In *Proceedings of Interspeech 2020*. **(check: full author list)**
- Sepp Hochreiter and Jürgen Schmidhuber. 1997. Long short-term memory. *Neural Computation*, 9(8):1735–1780. **(check)**
- Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. 2022. LoRA: Low-rank adaptation of large language models. In *Proceedings of ICLR 2022*. **(check)**
- Daniel Jurafsky and James H. Martin. *Speech and Language Processing*, 3rd edition draft, chapter 16. **(check: year of the draft used)**
- Yunpeng Liu, Xukui Yang, and Dan Qu. 2024. Exploration of Whisper fine-tuning strategies for low-resource ASR. *EURASIP Journal on Audio, Speech, and Music Processing*, 2024(1):29. doi:10.1186/s13636-024-00349-3.
- Tobi Olatunji et al. 2023. AfriSpeech-200: Pan-African accented speech dataset for clinical and general domain ASR. *Transactions of the Association for Computational Linguistics*, 11. **(check: full author list and pages)**
- Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine McLeavey, and Ilya Sutskever. 2023. Robust speech recognition via large-scale weak supervision. In *Proceedings of ICML 2023*, PMLR 202:28492–28518.
- Avinash Kumar Sharma, Manas R. Pandya, and Arpit Shukla. 2025. Fine-tuning Whisper Tiny for Swahili ASR: Challenges and recommendations for low-resource speech recognition. In *Proceedings of the Sixth Workshop on African Natural Language Processing (AfricaNLP 2025)*, pages 74–81. doi:10.18653/v1/2025.africanlp-1.11.
- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you need. In *Advances in Neural Information Processing Systems 30*. **(check)**
