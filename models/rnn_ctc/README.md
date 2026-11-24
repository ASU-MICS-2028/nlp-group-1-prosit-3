# M1: BiLSTM + CTC Baseline (`models/rnn_ctc`)

Owner: Bernard Marfo (Issue #4)

A stacked Bidirectional LSTM acoustic model trained from scratch with CTC loss on AfriSpeech-200 (`80`-band log-mel spectrograms at 16 kHz -> characters).

## Files

- `data.py`: character vocabulary (matching `common.score.normalize`), log-mel feature extraction, SpecAugment, and AfriSpeech-200 `train`/`dev` loader.
- `model.py`: `BiLSTMCTC` (optional 2-layer strided `Conv2d` 4x time-subsampling frontend) and `greedy_decode`.
- `train.py`: training loop with AdamW, gradient clipping, mixed precision on CUDA, dev WER/CER tracking, and epoch checkpointing/resume.
- `predict.py`: runs a saved checkpoint on all 1,000 clips in `common/test_set.csv` and writes `predictions.csv`.

## Running on Google Colab Pro (L4 / A100)

Select **Runtime -> Change runtime type -> L4 GPU (or A100 GPU)**, then run:

### Cell 1: Mount Drive, clone branch, install `uv` & sync
```python
from google.colab import drive
drive.mount("/content/drive")

!git clone -b 4-rnn-ctc-baseline https://github.com/ASU-MICS-2028/nlp-group-1-prosit-3.git /content/prosit3
%cd /content/prosit3
!pip install -q uv
!uv sync
```

### Cell 2: Run 1 — Baseline 3-layer BiLSTM (with 4x Conv2d subsampling)
```bash
!uv run python -m models.rnn_ctc.train \
  --out-dir /content/drive/MyDrive/prosit3-m1/run1-bilstm3-h256-sub \
  --epochs 20 --batch-size 32 --lr 1e-3 \
  --hidden-size 256 --num-layers 3 --dropout 0.2 \
  --subsample --resume
```

### Cell 3: Run 2 — Larger 4-layer BiLSTM + SpecAugment
```bash
!uv run python -m models.rnn_ctc.train \
  --out-dir /content/drive/MyDrive/prosit3-m1/run2-bilstm4-h512-sub-specaug \
  --epochs 25 --batch-size 32 --lr 1e-3 \
  --hidden-size 512 --num-layers 4 --dropout 0.3 \
  --subsample --spec-augment --resume
```

### Cell 4: Predict on the shared 1,000-clip test set and score
```bash
!uv run python -m models.rnn_ctc.predict \
  --checkpoint /content/drive/MyDrive/prosit3-m1/run1-bilstm3-h256-sub/best.pt \
  --out eval/results/m1-bilstm3-h256-sub/predictions.csv

!uv run python -m common.score eval/results/m1-bilstm3-h256-sub/predictions.csv
```

Copy `predictions.csv` and `scores.json` back into the repo (or commit directly from Colab), write `run.md`, and log the run in `docs/gpu-log.md`.
