# Results

Every result we report, one folder per run: `<run-name>/predictions.csv` (`audio_id,hypothesis`), `scores.json` (from `uv run python -m common.score`) and `run.md` (frontmatter: `title, model, owner, issue, wer, gpu, cost, date`). A number in the report must come from here. The table below is generated.

<!-- index -->

| Title | model | owner | wer |
|---|---|---|---|
| [Whisper-small zero-shot, greedy](m3-whisper-small-zeroshot/run.md) | openai/whisper-small | Joseph Etse | 0.480 |
| [Whisper-small zero-shot, temperature fallback](m3-whisper-small-zeroshot-fallback/run.md) | openai/whisper-small | Joseph Etse | 0.350 |
