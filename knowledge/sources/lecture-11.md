---
title: "Lecture 11: Why Experience Still Matters, AI in Ghana's Market, Enterprise Harnesses and Multi-Voice Text-to-Speech"
source: Lecture 11 recording
author: NLP Group 1
ai-use: Claude summarised the transcript; the team checks it before citing
---

# Lecture 11: Why Experience Still Matters, AI in Ghana's Market, Enterprise Harnesses and Multi-Voice Text-to-Speech

## In one paragraph
A short, informal recording (about 19 minutes) that seems to start partway through the session. It covers four conversations:
1. a debugging story about why experience still matters when you build with AI;
2. why Ghana's incumbent companies have little reason to adopt AI;
3. how US enterprises use AI models, and why custom harnesses are an opportunity;
4. a student's question about giving each character in a generated audiobook the right voice.

There was no formal teaching and nothing about deadlines. It ended with goodbyes before the instructor's trip. The speaker labels are inconsistent (one label is sometimes the instructor, sometimes a student) and the audio is often garbled, so who said what is often unclear.

Mis-transcriptions:
- "Finance engineering" is almost certainly harness engineering (from Lecture 10), and "the honest side" is the harness side.
- "Copy-paste models" seems to mean open-weight models.
- The voice models "Pro Pro", "FishQ"/"Fish" (perhaps Fish Speech) and "Chatbots" are unclear in the recording.
- So are "Opus 100", "Tesla or Blockchain" and "speech grammar".

## Key ideas, explained simply
- **Experience still matters.** A 10-minute timer ran out in seconds for about three students. The developer, a recent computing graduate, had spent one to two weeks prompting an AI without finding the cause. In one joint session, experience pointed to it within minutes: the device clock did not match the server's. The lesson: in a complex system too much can go wrong for prompting alone.
- **Why incumbents adopt AI slowly.** Large incumbents (MTN was the example, with its long queues) face little competition, so there is little pressure to innovate. Yet many of their service problems could be solved simply with AI assistants. Their real competition is the informal seller.
- **AI-first companies.** Selling AI to incumbents such as insurers is hard, because they are not interested. Building an AI-first insurer or bank could win, but needs capital and has to pass regulation.
- **How US enterprises use models:**
  - they license proprietary models under legal agreements that protect their data;
  - they use cloud-hosted copies (an OpenAI model run inside AWS, so data never goes to OpenAI);
  - they increasingly use open-weight models;
  - some build their own agentic or coding harness on top. He called custom harnesses one of the main opportunities for students.
- **Multi-voice audiobooks.** A student's first text-to-speech model skipped text and was not expressive, so they were trying other open models from Hugging Face on their own hardware. The suggested approach (apparently from the instructor, who had built something similar) had three steps:
  1. An LLM pre-processing pass links each line of dialogue to a character, since some lines are ambiguous. It also records details such as gender, from pronouns and context.
  2. Each character gets a fixed sample voice.
  3. That voice is used for the character throughout.
- **PDF-to-voice-note agent.** An agent on WhatsApp turns an uploaded PDF into a voice note. Speech APIs limit input size, so it sends the text in chunks and joins the audio. A student had found older models ran sentences together without punctuation. The reply: newer models handle pauses themselves, so workarounds can become unnecessary as models improve (like Lecture 10's "harness absorbed into the model").

## What the instructor said about assignments, deadlines or grading
Nothing about deadlines, grading, the viva or quizzes. The only logistics: goodbyes, and that he would see the class online, possibly Tuesday (unclear in the recording).

## Relevance to Prosit 3
- **Little direct relevance.** The audiobook discussion is text-to-speech, the opposite of speech recognition.
- **Chunking long input** and joining the outputs. Long dictations may need this, depending on how much audio each model accepts. Check this per model before relying on it.
- **Newer models need less pre-processing.** Test whether transcript normalisation (punctuation, casing) changes WER, rather than assuming.
- **Data privacy.** The licence versus self-hosting layers bear on the brief's patient-data concerns. Running wav2vec2 or Whisper on our own infrastructure keeps the audio in-house.
- **Experience still matters.** This backs Lecture 10's viva rule: understand the pipeline yourself when training or evaluation goes wrong.

## Likely quiz or viva questions
1. Why might Ghana's incumbents be slow to adopt AI? Little competition means little pressure to innovate.
2. Name two ways enterprises use proprietary models while protecting data. Licences with legal data protections, or cloud-hosted copies (for example, inside AWS).
3. How do you give each audiobook character a consistent voice? An LLM pre-processing step maps each dialogue line to a character, and each character gets a fixed sample voice.
4. How do you voice a long document when the API limits input? Chunk the text, synthesise each chunk, and join the audio.
5. Why can prompting fail where experience succeeds? Complex systems have many failure points, and experience tells you where to look (here, device time vs server time).
