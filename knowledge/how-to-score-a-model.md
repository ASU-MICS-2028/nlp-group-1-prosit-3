---
title: How to score a model on the shared test set
tags: [evaluation, howto, s0]
source: docs/decisions/0009-test-set-predictions-and-checkpoints.md, common/data.py, common/score.py
author: Joseph Etse
ai-use: Claude wrote the recipe from the S0 code; Joseph ran it end to end
---

# How to score a model on the shared test set

Every model (M1–M4) predicts on the same 1,000 clips and is scored by the same script, so the WERs are comparable ([[word-error-rate]]).

**1. Predict.** Write one row per test clip, all 1,000, each exactly once:

```python
import csv
from pathlib import Path
from common.data import fetch_test_audio, load_audio, load_test_set

out = Path("eval/results/m3-whisper-small-zeroshot")  # one folder per run
out.mkdir(parents=True, exist_ok=True)
paths = fetch_test_audio()            # first call writes 1,000 WAVs under data/ (about 6 GB download, once)
with open(out / "predictions.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["audio_id", "hypothesis"])
    for row in load_test_set():
        audio = load_audio(paths[row["audio_id"]])   # mono float32, 16 kHz
        w.writerow([row["audio_id"], my_model(audio)])
```

**2. Score.** `uv run python -m common.score eval/results/<run>/predictions.csv` prints WER and CER overall, by domain and by accent, and writes `scores.json` next to the predictions.

**3. Record.** Add `eval/results/<run>/run.md` with frontmatter `title`, `model`, `owner`, `wer` (the overall WER) and `ai-use`, saying what was run (checkpoint, settings, GPU time). Then run `python3 scripts/build_indexes.py`.

**Checks:** a copy of the transcripts as hypotheses scores WER 0.000. The scorer refuses a file with missing, duplicate or extra IDs. A blank hypothesis is allowed and counts as all words deleted.

Related: [[word-error-rate]], [[afrispeech-200]], [[environment]]
