"""Character vocabulary, log-mel features, SpecAugment, and AfriSpeech-200 dataset for M1."""

import io
import random
from collections.abc import Sequence

import librosa
import numpy as np
import pyarrow.parquet as pq
import soundfile as sf
import torch
from torch.utils.data import Dataset

from common.data import split_files
from common.score import normalize

SAMPLE_RATE = 16_000
N_MELS = 80
N_FFT = 400       # 25 ms at 16 kHz
HOP_LENGTH = 160  # 10 ms at 16 kHz

BLANK_IDX = 0
CHARS = " abcdefghijklmnopqrstuvwxyz0123456789'"
VOCAB = ["<blank>", *CHARS]
CHAR_TO_ID = {ch: idx + 1 for idx, ch in enumerate(CHARS)}
ID_TO_CHAR = {idx + 1: ch for idx, ch in enumerate(CHARS)}


def text_to_ids(text: str) -> list[int]:
    """Normalize text the same way as common.score and map characters to token IDs."""
    clean = normalize(text)
    return [CHAR_TO_ID[ch] for ch in clean if ch in CHAR_TO_ID]


def ids_to_text(ids: Sequence[int]) -> str:
    """Convert non-blank token IDs back into a string."""
    return "".join(ID_TO_CHAR[i] for i in ids if i in ID_TO_CHAR)


def decode_audio_bytes(raw_bytes: bytes, target_sr: int = SAMPLE_RATE) -> np.ndarray:
    """Decode WAV/FLAC bytes in memory to mono float32 at 16 kHz."""
    audio, sr = sf.read(io.BytesIO(raw_bytes), dtype="float32")
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    if sr != target_sr:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
    return audio.astype(np.float32, copy=False)


def waveform_to_log_mel(audio: np.ndarray, sr: int = SAMPLE_RATE, n_mels: int = N_MELS) -> torch.Tensor:
    """Turn a 1D waveform into a per-clip normalized log-mel spectrogram of shape (time, n_mels)."""
    if audio.size == 0 or not np.isfinite(audio).all():
        raise ValueError("Audio waveform is empty or contains non-finite values.")
    mel = librosa.feature.melspectrogram(
        y=audio,
        sr=sr,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        win_length=N_FFT,
        n_mels=n_mels,
        fmin=0.0,
        fmax=sr / 2.0,
    )
    log_mel = np.log(mel + 1e-6).T  # (time, n_mels)
    mean = log_mel.mean()
    std = log_mel.std()
    log_mel = (log_mel - mean) / (std + 1e-6)
    return torch.from_numpy(log_mel.astype(np.float32, copy=False))


def spec_augment(
    features: torch.Tensor,
    freq_mask_param: int = 12,
    time_mask_param: int = 35,
    num_freq_masks: int = 2,
    num_time_masks: int = 2,
) -> torch.Tensor:
    """Simple SpecAugment: zero out random frequency bands and time spans on (time, n_mels)."""
    augmented = features.clone()
    num_frames, num_mels = augmented.shape
    for _ in range(num_freq_masks):
        width = random.randint(0, min(freq_mask_param, num_mels))
        if width > 0:
            start = random.randint(0, num_mels - width)
            augmented[:, start : start + width] = 0.0
    for _ in range(num_time_masks):
        width = random.randint(0, min(time_mask_param, max(1, num_frames // 5)))
        if width > 0 and num_frames > width:
            start = random.randint(0, num_frames - width)
            augmented[start : start + width, :] = 0.0
    return augmented


class AfriSpeechCTCDataset(Dataset):
    """Loads AfriSpeech-200 train or dev clips from the pinned parquet mirror."""

    def __init__(
        self,
        split: str,
        max_clips: int | None = None,
        max_duration_s: float = 20.0,
        subsample_factor: int = 1,
        augment: bool = False,
    ) -> None:
        if split not in {"train", "dev"}:
            raise ValueError(f"Training/validation split must be 'train' or 'dev', got {split!r}")
        self.augment = augment
        self.samples: list[dict] = []

        for parquet_path in split_files(split):
            table = pq.read_table(parquet_path, columns=["audio_id", "audio", "transcript", "duration"])
            for row in table.to_pylist():
                duration = float(row.get("duration") or 0.0)
                if duration <= 0.1 or duration > max_duration_s:
                    continue
                target_ids = text_to_ids(row.get("transcript") or "")
                if not target_ids:
                    continue
                # Conservative frame check so CTC input length T >= target length U.
                approx_frames = int(duration * SAMPLE_RATE / HOP_LENGTH) // subsample_factor
                if approx_frames < len(target_ids) + 2:
                    continue
                self.samples.append({
                    "audio_id": row["audio_id"],
                    "audio_bytes": row["audio"]["bytes"],
                    "transcript": normalize(row["transcript"]),
                    "target_ids": target_ids,
                })
                if max_clips is not None and len(self.samples) >= max_clips:
                    return

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> dict:
        sample = self.samples[idx]
        audio = decode_audio_bytes(sample["audio_bytes"])
        features = waveform_to_log_mel(audio)
        if self.augment:
            features = spec_augment(features)
        return {
            "audio_id": sample["audio_id"],
            "features": features,
            "target_ids": torch.tensor(sample["target_ids"], dtype=torch.long),
            "transcript": sample["transcript"],
        }


def collate_ctc_batch(batch: list[dict]) -> dict:
    """Pad variable-length spectrograms and pack 1D targets for torch.nn.CTCLoss."""
    batch_size = len(batch)
    n_mels = batch[0]["features"].shape[1]
    feature_lengths = torch.tensor([item["features"].shape[0] for item in batch], dtype=torch.long)
    max_time = int(feature_lengths.max().item())

    padded = torch.zeros(batch_size, max_time, n_mels, dtype=torch.float32)
    for i, item in enumerate(batch):
        t = item["features"].shape[0]
        padded[i, :t, :] = item["features"]

    target_lengths = torch.tensor([len(item["target_ids"]) for item in batch], dtype=torch.long)
    targets = torch.cat([item["target_ids"] for item in batch], dim=0)

    return {
        "features": padded,
        "feature_lengths": feature_lengths,
        "targets": targets,
        "target_lengths": target_lengths,
        "transcripts": [item["transcript"] for item in batch],
        "audio_ids": [item["audio_id"] for item in batch],
    }
