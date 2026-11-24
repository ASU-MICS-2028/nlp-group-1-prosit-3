---
title: "M1: RNN baseline (BiLSTM + CTC)"
owner: Bernard Marfo
issue: "#4"
status: doing
ai-use: Antigravity drafted the initial plan structure from issue #4, AGENTS.md, and S0; Bernard reviewed and approved starting
---

# Plan for #4: M1: RNN baseline (BiLSTM + CTC)

## Goal

Build and fairly test the consultant's recommendation: a BiLSTM acoustic model trained from scratch with CTC loss on AfriSpeech-200 (log-mel spectrogram in, English characters out). Its WER and CER on `common/test_set.csv` provide the team's direct evidence for or against RNNs in the report.

## Steps

1. **Environment and dependencies:** Run `uv sync`, add `torch` (with a decision record in `docs/decisions/`), and confirm existing tests pass with `uv run pytest`.
2. **Vocabulary, features, and data loader (`models/rnn_ctc/data.py`):** Define the character vocabulary (lowercase `a-z`, digits `0-9`, apostrophe, space, plus CTC blank), extract 80-band log-mel spectrograms at 16 kHz (25 ms window, 10 ms hop), and load AfriSpeech-200 `train` and `dev` splits via `common.data.split_files` (never reading `test`).
3. **BiLSTM + CTC model and decoder (`models/rnn_ctc/model.py`):** Implement the smallest clean BiLSTM acoustic model + greedy CTC decoder, with unit tests in `tests/test_rnn_ctc.py` covering tensor shapes, CTC length checks, and greedy collapse logic.
4. **CPU overfit sanity check (`models/rnn_ctc/train.py`):** Overfit a tiny subset (8–16 training clips) on local CPU until CTC loss approaches zero and greedy decoding recovers the transcripts, confirming no pipeline bugs before using paid GPU time.
5. **Baseline GPU training run:** Train the baseline BiLSTM + CTC model on AfriSpeech-200 `train`, monitor `dev` WER/CER, save the best checkpoint off-repo, and log the run in `docs/gpu-log.md`.
6. **Compare alternatives:** Run controlled comparisons (subsampling frontend, SpecAugment / capacity, decoding) using the same training/dev splits and score each kept run on `common/test_set.csv`.
7. **Final test-set evaluation (`models/rnn_ctc/predict.py`):** Generate `eval/results/<run>/predictions.csv` on all 1,000 test clips, run `uv run python -m common.score`, and write `eval/results/<run>/run.md`.
8. **Write-up and PR:** Log atomic findings in `learnings/` (including options that lost), draft the Section B subsection and slide segment, fill in `docs/changes/4-rnn-ctc-baseline.md`, rebuild indexes, and open a PR.

## Alternatives to compare

All kept models are evaluated on the exact same `common/test_set.csv` with `uv run python -m common.score`:

- **Time subsampling frontend:** Raw 10 ms mel frames fed straight into BiLSTM vs. a lightweight 2-layer strided Conv2d frontend (4x time downsampling, which speeds up BiLSTM training and helps CTC alignment on long clips).
- **Model capacity and regularisation:** Compact 3-layer BiLSTM (hidden 256, dropout 0.2) vs. larger 4-layer BiLSTM (hidden 512) with SpecAugment (time + frequency masking).
- **Decoding:** Greedy CTC decoding (no external LM) vs. CTC beam search (and optionally an n-gram LM if beam search alone leaves clear spelling gains on the table; adding a decoding library would get a decision record first).

## Failure cases

- **CTC input shorter than target (`T < U`):** Causes infinite/NaN CTC loss on very short clips or long transcripts. Mitigate by filtering out invalid clips (`T < U`), using `CTCLoss(zero_infinity=True)`, and adding a unit test.
- **Empty transcripts or silent/corrupt audio:** Filter empty transcripts and guard against zero-length or NaN waveforms in the dataset loader; test in `tests/test_rnn_ctc.py`.
- **Exploding gradients / diverging RNN training:** Apply gradient norm clipping (`clip_grad_norm_`), AdamW, and a learning rate schedule; verify loss decreases monotonically on the CPU overfit check.
- **GPU out-of-memory (OOM) on long clips:** Cap maximum training clip length (e.g., 20–25 s) and bucket/sort batches by duration so padding stays small.
- **Interrupted GPU run / network drop:** Save checkpoints every epoch (weights, optimizer, epoch, best dev WER) so training can resume cleanly.
- **Test set leakage:** Keep `common/test_set.csv` strictly out of `train.py`; only `predict.py` reads `load_test_set()`.

## GPU cost estimate

- **Local CPU (development, unit tests, 8–16 clip overfit sanity check):** \$0.00.
- **Google Colab Pro (Bernard's personal subscription; L4 24 GB or A100 40 GB, checkpoints saved to Google Drive):** \$0.00 on the shared team GPU account.
  - Run 1 (baseline BiLSTM + CTC): ~2–4 hours on L4 / ~1–2 hours on A100
  - Run 2 (Conv2d subsampling + SpecAugment / larger BiLSTM): ~3–5 hours on L4 / ~1.5–2.5 hours on A100
  - Test-set inference (1,000 clips): < 5 minutes
  - Actual runtime and hardware will still be logged in `docs/gpu-log.md` after every run (marked Colab Pro, \$0 shared cost).

## Done when

- [ ] `eval/results/<run>/predictions.csv` and `run.md` exist for every run you report, and `scores.json` was produced by `uv run python -m common.score`
- [ ] Learnings written in `learnings/`, one finding per file, including the options that lost
- [ ] Section B subsection drafted (about half a page; length still pending, decision 0006) and your slide segment added
- [ ] Every GPU run logged in `docs/gpu-log.md`
- [ ] Change file in `docs/changes/` and PR merged
