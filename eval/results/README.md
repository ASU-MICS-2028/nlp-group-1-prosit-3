# Results

Every result we report, one folder per run: `<run-name>/predictions.csv` (`audio_id,hypothesis`), `scores.json` (from `uv run python -m common.score`) and `run.md` (frontmatter: `title, model, owner, issue, wer, gpu, cost, date`). A number in the report must come from here. The table below is generated.

<!-- index -->

| Title | model | owner | wer |
|---|---|---|---|
| [Kaggle trial run: 20 training steps, then predict and score the test set](m3-kaggle-smoke/run.md) | openai/whisper-small (20 steps, effectively untrained) | Joseph Etse | 0.341 (not a fine-tuning result) |
| [Whisper-base zero-shot, temperature fallback](m3-whisper-base-zeroshot-fallback/run.md) | openai/whisper-base | Joseph Etse | 0.464 |
| [Whisper-large-v3-turbo zero-shot, temperature fallback](m3-whisper-large-v3-turbo-zeroshot-fallback/run.md) | openai/whisper-large-v3-turbo | Joseph Etse | 0.293 |
| [Whisper-small fully fine-tuned on AfriSpeech-200 (4,000 steps, Kaggle T4)](m3-whisper-small-afrispeech/run.md) | openai/whisper-small, all weights fine-tuned | Joseph Etse | 0.156 |
| [Whisper-small fully fine-tuned on AfriSpeech-200 (8,000 steps, Kaggle T4)](m3-whisper-small-afrispeech-8k/run.md) | openai/whisper-small, all weights fine-tuned | Joseph Etse | 0.152 |
| [Whisper-small zero-shot, greedy](m3-whisper-small-zeroshot/run.md) | openai/whisper-small | Joseph Etse | 0.480 |
| [Whisper-small zero-shot, temperature fallback](m3-whisper-small-zeroshot-fallback/run.md) | openai/whisper-small | Joseph Etse | 0.350 |
| [Whisper-small zero-shot, temperature fallback, language detected](m3-whisper-small-zeroshot-fallback-detect/run.md) | openai/whisper-small | Joseph Etse | 0.464 |
| [Whisper-tiny zero-shot, temperature fallback](m3-whisper-tiny-zeroshot-fallback/run.md) | openai/whisper-tiny | Joseph Etse | 0.571 |
| [Kaggle notebook: extra zero-shot runs (tiny, base, small with language detection)](m3-whisper-zeroshot-extra/run.md) |  | Joseph Etse |  |
