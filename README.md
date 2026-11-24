# Prosit 3: Dictation for Ayamra Hospitals (Speech Recognition with Transformers)

ICS554 Natural Language Processing, Ashesi University. NLP Group 1: Michael Boadi, Joseph Etse, Alice Kara-Acquah, Bernard Marfo, Eric Sunu.

Ayamra is a network of hospitals in major African cities. Its doctors spend too long writing notes and want to dictate them instead. A consultant suggested a recurrent neural network (RNN) trained on the AfriSpeech-200 dataset. We test that advice: we train an RNN and three transformer models on the same data, score them all on the same 1,000 test clips (clinical and general speech, many African accents), recommend one, and build a small dictation demo on it.

## Results at a glance

Coming soon. Every number will come from a saved file in [`eval/results/`](eval/results/README.md).

## Who does what

| Slot | What | Owner |
|---|---|---|
| S0 | Fixed test set and shared scorer | Joseph |
| M1 | RNN baseline (BiLSTM + CTC) | Bernard |
| M2 | wav2vec2 fine-tune (CTC) | Alice |
| M3 | Whisper zero-shot and full fine-tune | Joseph |
| M4 | Whisper + LoRA | Eric |
| M5 | Dictation demo, error analysis, report and slides | Michael |

Work is tracked in [GitHub issues](https://github.com/ASU-MICS-2028/nlp-group-1-prosit-3/issues). Each issue has a plan in [`docs/plans/`](docs/plans/README.md), and each merged change has a file in [`docs/changes/`](docs/changes/README.md) saying who did it and how AI was used.

## Folder guide

| Folder | What is in it |
|---|---|
| [`knowledge/`](knowledge/README.md) | What the team knows, one idea per file: lectures, the brief, ASR concepts, setup |
| [`learnings/`](learnings/README.md) | What we found while building, one finding per file, including the options that lost |
| [`docs/decisions/`](docs/decisions/README.md) | Numbered decision records |
| [`docs/plans/`](docs/plans/README.md), [`docs/changes/`](docs/changes/README.md) | One plan per issue; one change record per merged PR |
| `common/` | The test set, audio access and the scorer every model uses |
| `models/` | One folder per model (M1–M4) |
| `demo/` | The dictation demo (M5) |
| `report/` | The ACL-format report |
| [`eval/results/`](eval/results/README.md) | Every saved result |

Slides live in the group's shared Drive (`NLP-GROUP-1/prosit 3/`).

## Running it

Setup is in [`knowledge/environment.md`](knowledge/environment.md). In short: install [uv](https://docs.astral.sh/uv/), run `uv sync`, and run `git config core.hooksPath .githooks`.

## Data licence

[AfriSpeech-200](https://huggingface.co/datasets/intronhealth/afrispeech-200) by Intron Health, CC BY-NC-SA 4.0, for research use. We download it from the public copy [evie-8/afrispeech-200](https://huggingface.co/datasets/evie-8/afrispeech-200) because access to the official repo was not granted; Dr. Asamoah approved this (decision 0010). `common/test_set.csv` contains transcripts from its test split under the same licence. We make no attempt to identify speakers.
