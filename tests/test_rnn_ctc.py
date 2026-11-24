"""Unit tests and synthetic CPU overfit check for M1 (BiLSTM + CTC)."""

import numpy as np
import pytest
import torch
import torch.nn as nn

from models.rnn_ctc.data import (
    AfriSpeechCTCDataset,
    BLANK_IDX,
    CHAR_TO_ID,
    N_MELS,
    SAMPLE_RATE,
    VOCAB,
    collate_ctc_batch,
    ids_to_text,
    spec_augment,
    text_to_ids,
    waveform_to_log_mel,
)
from models.rnn_ctc.model import BiLSTMCTC, greedy_decode


def test_vocab_roundtrip_matches_scorer_normalization() -> None:
    ids = text_to_ids("His mother is in her 50 s, and has hypertension.")
    assert BLANK_IDX not in ids
    assert ids_to_text(ids) == "his mother is in her 50s and has hypertension"


def test_waveform_to_log_mel_shape_and_guards() -> None:
    audio = np.sin(np.linspace(0, 200 * np.pi, SAMPLE_RATE, dtype=np.float32))
    mel = waveform_to_log_mel(audio)
    assert mel.ndim == 2
    assert mel.shape[1] == N_MELS
    assert mel.shape[0] > 90  # ~100 frames for 1 second at 10 ms hop

    with pytest.raises(ValueError):
        waveform_to_log_mel(np.array([], dtype=np.float32))
    with pytest.raises(ValueError):
        waveform_to_log_mel(np.array([0.0, np.nan, 0.1], dtype=np.float32))


def test_spec_augment_preserves_shape_without_mutating_input() -> None:
    original = torch.ones(80, N_MELS)
    augmented = spec_augment(original)
    assert augmented.shape == original.shape
    assert torch.equal(original, torch.ones(80, N_MELS))


def test_dataset_rejects_test_split() -> None:
    with pytest.raises(ValueError):
        AfriSpeechCTCDataset(split="test")


@pytest.mark.parametrize("subsample", [False, True])
def test_bilstm_ctc_forward_shapes(subsample: bool) -> None:
    model = BiLSTMCTC(hidden_size=32, num_layers=2, dropout=0.1, subsample=subsample)
    batch = collate_ctc_batch([
        {"audio_id": "a", "features": torch.randn(100, N_MELS), "target_ids": torch.tensor([1, 2, 3]), "transcript": "abc"},
        {"audio_id": "b", "features": torch.randn(60, N_MELS), "target_ids": torch.tensor([4, 5]), "transcript": "de"},
    ])
    log_probs, out_lens = model(batch["features"], batch["feature_lengths"])
    expected_t = int(out_lens.max().item())
    assert log_probs.shape == (expected_t, 2, len(VOCAB))
    assert (out_lens > 0).all()


def test_greedy_decode_merges_repeats_and_keeps_double_letters() -> None:
    # Sequence: h h _ e _ l l _ l l _ o o -> "hello"
    h, e, l, o = CHAR_TO_ID["h"], CHAR_TO_ID["e"], CHAR_TO_ID["l"], CHAR_TO_ID["o"]
    seq = [h, h, BLANK_IDX, e, BLANK_IDX, l, l, BLANK_IDX, l, l, BLANK_IDX, o, o]
    log_probs = torch.full((len(seq), 1, len(VOCAB)), -10.0)
    for t, tok in enumerate(seq):
        log_probs[t, 0, tok] = 0.0
    lengths = torch.tensor([len(seq)], dtype=torch.long)
    assert greedy_decode(log_probs, lengths) == ["hello"]


def test_cpu_overfit_synthetic_batch() -> None:
    """Proves the BiLSTM + CTC pipeline can drive CTC loss near zero and recover exact text."""
    torch.manual_seed(0)
    model = BiLSTMCTC(hidden_size=64, num_layers=1, dropout=0.0, subsample=True)
    criterion = nn.CTCLoss(blank=BLANK_IDX, zero_infinity=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-3)

    t1 = "dose"
    t2 = "pain"
    # Synthetic spectrograms with distinct time-frequency segments (like phonemes).
    f1 = torch.zeros(64, N_MELS)
    f2 = torch.zeros(72, N_MELS)
    for idx in range(4):
        f1[idx * 16 : (idx + 1) * 16, idx * 10 : (idx + 1) * 10] = 2.0
        f2[idx * 18 : (idx + 1) * 18, 40 + idx * 10 : 40 + (idx + 1) * 10] = 2.0

    batch = collate_ctc_batch([
        {"audio_id": "s1", "features": f1, "target_ids": torch.tensor(text_to_ids(t1)), "transcript": t1},
        {"audio_id": "s2", "features": f2, "target_ids": torch.tensor(text_to_ids(t2)), "transcript": t2},
    ])

    initial_loss = None
    final_loss = None
    for _ in range(150):
        optimizer.zero_grad()
        log_probs, out_lens = model(batch["features"], batch["feature_lengths"])
        loss = criterion(log_probs, batch["targets"], out_lens, batch["target_lengths"])
        if initial_loss is None:
            initial_loss = float(loss.item())
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), 5.0)
        optimizer.step()
        final_loss = float(loss.item())
        if final_loss < 0.02:
            break

    assert initial_loss is not None and final_loss is not None
    assert final_loss < 0.05
    model.eval()
    with torch.no_grad():
        log_probs, out_lens = model(batch["features"], batch["feature_lengths"])
        preds = greedy_decode(log_probs, out_lens)
    assert preds == [t1, t2]
