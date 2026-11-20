"""The fixed test set and its audio. Every model predicts with the same loop:

    from common.data import fetch_test_audio, load_audio, load_test_set
    paths = fetch_test_audio()
    for row in load_test_set():
        hyp = model(load_audio(paths[row["audio_id"]]))

Data comes from the public AfriSpeech-200 mirror evie-8/afrispeech-200 (decision 0010),
pinned to one revision so everyone gets the same files.
"""

import csv
import glob
from pathlib import Path

import librosa
import numpy as np
import pyarrow.parquet as pq
from huggingface_hub import snapshot_download

REPO = "evie-8/afrispeech-200"
REVISION = "cafdc16d1e1dcfcd2b599c00b1ea44d5624db08f"
TEST_SET = Path(__file__).with_name("test_set.csv")


def split_files(split: str) -> list[str]:
    """Download (once, into the Hugging Face cache) and return the parquet files of one split."""
    root = snapshot_download(REPO, repo_type="dataset", revision=REVISION, allow_patterns=[f"data/{split}-*"])
    return sorted(glob.glob(f"{root}/data/{split}-*.parquet"))


def read_split(split: str, columns: list[str]) -> list[dict]:
    """The chosen columns of one split ("train", "dev" or "test"), one dict per clip."""
    return [row for f in split_files(split) for row in pq.read_table(f, columns=columns).to_pylist()]


def load_test_set(path: Path = TEST_SET) -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def fetch_test_audio(dest: Path = Path("data/afrispeech-test")) -> dict[str, Path]:
    """Write the test-set clips to dest as WAV files and return audio_id -> path. A second call writes nothing."""
    ids = {r["audio_id"] for r in load_test_set()}
    paths = {i: Path(dest) / f"{i}.wav" for i in ids}  # audio_id is "<speaker>/<clip>", so one folder per speaker
    if not all(p.exists() for p in paths.values()):
        for f in split_files("test"):
            for row in pq.read_table(f, columns=["audio_id", "audio"]).to_pylist():
                if row["audio_id"] in ids:
                    paths[row["audio_id"]].parent.mkdir(parents=True, exist_ok=True)
                    paths[row["audio_id"]].write_bytes(row["audio"]["bytes"])
    missing = sorted(i for i, p in paths.items() if not p.exists())
    if missing:
        raise FileNotFoundError(f"{len(missing)} test clips have no audio, e.g. {missing[:5]}")
    return paths


def load_audio(path: Path) -> np.ndarray:
    """Mono float32 at 16 kHz, what every model here expects."""
    return librosa.load(path, sr=16000, mono=True)[0]
