---
title: "Lecture 12: Speech Recognition Basics (Challenges, Mel Spectrograms, CNNs, RNNs, Encoder-Decoder); Prosit 3 Launch"
source: Lecture 12 recording (2026-11-09)
author: NLP Group 1
ai-use: Claude summarised the transcript; the team checks it before citing
---

# Lecture 12: Speech Recognition Basics; Prosit 3 Launch

## In one paragraph
This lecture starts the voice part of the course and launches Prosit 3. The instructor said that so far the course has worked with text, and now adds a second modality: speech. He suggested framing any deep learning problem by its input and output (speech to text, text to speech, image to text), because that tells you what to read. The class will focus on automatic speech recognition (ASR): a waveform goes in, text comes out. He listed the main challenges of ASR (domain, task, vocabulary size, channel and noise, speaker characteristics, code-switching). He explained how audio becomes numbers and then a mel spectrogram, and why aligning text with audio is the new problem. He then gave intuitions for CNNs (really cross-correlation), RNNs, encoder-decoders and GANs. From about minute 58 he read the Prosit 3 brief (Ayamra), the deliverables and the grading. He said whether the report is individual and how it is structured, and pointed to chapters 15, 16 and 17 (mostly 16). A quiz was mentioned for next week. The last half of the recording (from about minute 73) is after-class chat (unrelated discussion omitted).

Mis-transcriptions: "faucet", "deposits" and "process" are Prosit. "AYAMRA" is Ayamra and "AFISPEACH200" is AfriSpeech-200. "Tabulary science" and "vocabulary science" mean vocabulary size. "ML spectrum now" is mel spectrogram. "Kennel" is kernel. "Generative atmosphere" is generative adversarial networks (he names them correctly a moment later), and "stable distribution" is stable diffusion. "The English we speak in a crowd" is almost certainly "in Accra". The sample rates were transcribed as "16 Hz or 8 Hz": these are almost certainly **16 kHz and 8 kHz**, so check before citing.

## Key ideas, explained simply
- **The task shapes the system.** A voice assistant (Siri) takes voice in, transcribes it, finds the intent and takes an action. A courtroom transcription tool only transcribes (and maybe summarises), so intent does not matter. Speech in one language to text in another is speech translation, a different problem again. He guessed Siri listens passively for keywords, while a conversational model must listen actively ("I can't engineer Siri, but it's probably a passive listening process").
- **Challenges in ASR:**
  1. **Domain.** Medical and legal speech use their own words, so "the technology would have to behave differently".
  2. **Task.** Transcription, translation, or understanding to take an action.
  3. **Vocabulary size.** A system that recognises the digits 0 to 9 has few options; Siri's commands are still a limited set; a high court or a hospital makes the vocabulary "explode". Smaller vocabularies are easier.
  4. **Channel and noise.** The environment and the device. He told of a team that built a hospital ASR system with high accuracy in their own room; at their first client, a hospital near a main road, traffic noise made it "absolutely useless", and removing the background noise took six months.
  5. **Sampling rate.** Devices sample audio at different rates (stated as "16 Hz, right, or 8 Hz"; see the note above). A model can work on one device and fail in production on another. He also said "the number of Hz divided by 2"; what that refers to is not explained in the recording.
  6. **Speaker characteristics.** Accent, language, age ("the model that you train on for 50-year-olds will probably not work" for children), ethnicity and location all change the waveform. His example: the English spoken in Accra differs from the English spoken in Nigeria, and he stressed this is about accent and intonation, not one being better.
  7. **Code-switching.** People who speak a colonial language often mix in their local language. He called it "its own research problem": a model built "in San Francisco for English" will not handle it, and "even whisper and all those stuff, they are not so great when it comes to code-switching" unless it is in the data.
  Handling accents is "an actively researched problem", and he wants to see what approaches groups try.
- **From sound to numbers.** A microphone turns air-pressure changes into numbers: the raw waveform, an array that starts near 0 before speech begins. It is usually turned into a **mel spectrogram**, which "looks more like a matrix", and that is what models work with. Libraries produce these for you.
- **Alignment is the new part.** The text side uses the NLP we already know. The new challenge is aligning the text with the audio: where there is no sound, there should be no text.
- **RNNs** suit anything sequential, such as text ("I am going to school"). He called them "key in this particular" Prosit.
- **CNNs** suit grid-like data. An image is a grid of pixels; a waveform is a one-dimensional grid of numbers, so a 1D CNN can run on it. Worked example: a kernel (e.g. 0, 1, 0, 1) slides over the input and takes a dot product at each position; a bigger dot product means the two are more alike, and the results form a new matrix. Strictly this is **cross-correlation**: true convolution flips the kernel first, CNNs skip the flip, and the name is "for historical reasons".
- **CNNs as feature extractors.** In speech they pick up acoustic characteristics and phonemes. "For most speech" pipelines, convolution comes first, then the features go to other layers such as an RNN. Learned features in deep CNNs are usually not interpretable (early vision papers could show layer-by-layer features; today's models are too deep). An example he gave about a shared trait leaving a signal in recordings is unclear in the recording.
- **Encoder and decoder.** The encoder compresses the input into a latent space; the decoder generates output from it. His analogy (he said not to quote it): the mean of everyone's age is a compact representation of all their ages. Encoder-decoders are typical for machine translation ("bonjour" to "hello"), but encoder-only, decoder-only and encoder-decoder generation all exist, as do autoencoders.
- **GANs.** Two networks: one generates fakes, the other tries to catch them, and they train against each other. Once state of the art for images, now largely replaced by stable diffusion.
- **New voice-only models.** A student asked about a recently released voice-only model (name unclear in the recording). He had not read how it works, but said any such model still rests on the same foundations: spectrograms, acoustics, phonemes. "The approaches may change, but the foundation is always the same."

## What the instructor said about assignments, deadlines or grading
- **The brief (Ayamra).** A network of hospitals in many African cities wants doctors to dictate notes instead of writing them. A consultant suggested recurrent neural networks and the open AfriSpeech-200 dataset. We are the AI technologist. Questions: what RNNs are and how they solve the problem; whether RNNs are the best approach, with strengths and weaknesses against other approaches; would we recommend RNNs, and if not, what instead and why; and build the speech-to-text system following our recommendation.
- **Yes or no are both allowed.** "It could be that the answer is yes. It could be that the answer is no... So don't blindly say yes. If you say yes, you should have a reason. If you say no, you should have a reason." And: "Go and sit down and come back and tell us we are wrong... Or we are right. Or something in between."
- **Start with the RNN.** "So please do the RNN one. Start with the RNN, right? Because there's a reason why you're doing the RNN. But you can also look into CNNs."
- **Report format:** "the report format should be similar to what is used in ACL or other NLP publications and should be under 10 pages". It must make "a convincing scholarly case" for RNNs or for our alternative.
- **Individual report, group work** (about minute 64): "For the report. The report is individual. The report has always been individual, right?" ... "We have section A that's individual and then section B." ... "No, you work as a group and your report is individual." What "section B" is was not said.
- **The team must agree on one approach:** "you are working with a team... what's the capital of Ghana? Like it's Accra, right?... we've used Accra to work and do our calculations and everything, then in your report, you come and say that no, it's Lagos. There's a big problem. Either you didn't help the team or they were all wrong and you were right." And: "Either way, you're going to decide as a group because you're going to implement it together."
- **Not settled:** when a student kept asking about "section A and then technical report", he said "I'll confirm this with [the brief's author]. [The brief's author] prepared it." He added that the brief was sent to him the night before. Check the confirmed structure before writing.
- **Deliverables:** a team presentation; upload code to GitHub; "The first [slide]... should have the link to the GitHub code"; upload the slides to Canvas.
- **Grading:** group presentation 20%, technical report 45%, viva 35%.
- **Reading:** "the information you need mostly is within Chapter 15, 16, 17. But it's mostly 16 because this is an ASR problem. You are not generating text." He called the lecture "a crash course in Chapter 16", and urged focus: "you don't need everything."
- **Noise is not our problem this time:** "For this particular [Prosit], I don't think you'll have that problem because you'll work on your laptop", but it would fail in a real work environment.
- **Quiz:** a quiz appears to be next week, apparently Thursday (the exchange is unclear in the recording). Students asked for a study guide; none was promised, and he said he sometimes sees the questions at the same time as students.
- **Last Prosit's marking:** he noted some answers said encoder-only models can generate, which he agreed is possible.

## Relevance to Prosit 3
- **Our four systems fit his framing.** A BiLSTM+CTC model is the RNN he asked us to start with. wav2vec2 starts with a convolutional feature encoder, matching his "convolution first, then other layers" picture. Whisper (full fine-tune and +LoRA) is an encoder-decoder on mel spectrograms. Whisper's weakness on code-switching, which he named, is worth testing on AfriSpeech-200.
- **Comparison criteria come straight from the challenges list:** domain vocabulary (clinical words), accents and speaker traits (AfriSpeech-200 is accented African English), noise and channel, and sampling rate (resample everything to one rate; the 16 kHz / 8 kHz point).
- **Alignment** is the problem CTC solves for the RNN; say so in the report.
- **One shared recommendation.** Each report is individual but must agree with what the team built (the Accra/Lagos point).
- **Report:** ACL style, under 10 pages, with a scholarly case. Confirm the section A / section B structure.

## Likely quiz or viva questions
1. Name four challenges in ASR. Domain, vocabulary size, channel and noise (including sampling rate), speaker characteristics; also task and code-switching.
2. Why is a digit recogniser easier than a courtroom transcriber? Its vocabulary is tiny (0 to 9); a courtroom's explodes.
3. What is a mel spectrogram? A matrix representation computed from the raw waveform, which models work with.
4. What is the alignment problem? Matching text to the right stretch of audio, so silence maps to no text.
5. Why is a CNN "really" cross-correlation? It slides the kernel without flipping it; true convolution flips it.
6. Why put a CNN before an RNN for speech? The CNN extracts features (acoustic traits, phonemes); the RNN models the sequence.
7. What do an encoder and a decoder do? The encoder compresses input into a latent space; the decoder generates output from it.
8. Why might a model that works in testing fail in production? Different noise, devices or sampling rates, or speakers unlike the training data.
9. Must we recommend RNNs? No. Either answer is fine if justified, but the team must agree because it builds one system.
