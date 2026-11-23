import numpy as np
import pytest

from common.data import fetch_test_audio, load_audio, load_test_set


def test_test_set_shape():
    rows = load_test_set()
    assert len(rows) == 1000
    assert list(rows[0]) == ["audio_id", "transcript", "domain", "accent", "duration"]
    assert len({r["audio_id"] for r in rows}) == 1000
    assert sum(r["domain"] == "clinical" for r in rows) == 500
    assert sum(r["domain"] == "general" for r in rows) == 500
    assert all(r["transcript"].strip() for r in rows)


@pytest.mark.network
def test_fetch_and_load_audio(tmp_path):
    paths = fetch_test_audio(tmp_path)
    assert len(paths) == 1000
    for row in load_test_set()[:3]:
        audio = load_audio(paths[row["audio_id"]])
        assert audio.ndim == 1 and audio.dtype == np.float32
        assert len(audio) > 0.5 * 16000
    assert fetch_test_audio(tmp_path) == paths  # second call reuses the files


def test_split_files_limit_downloads_only_the_first_files(monkeypatch, tmp_path):
    import common.data as data
    names = [f"data/train-{i:05d}-of-00028.parquet" for i in range(28)] + ["data/dev-00000-of-00006.parquet"]
    monkeypatch.setattr(data, "list_repo_files", lambda *a, **k: names)
    asked = {}

    def fake_download(*a, allow_patterns, **k):
        asked["patterns"] = allow_patterns
        for p in allow_patterns:
            (tmp_path / p).parent.mkdir(parents=True, exist_ok=True)
            (tmp_path / p).touch()
        return str(tmp_path)

    monkeypatch.setattr(data, "snapshot_download", fake_download)
    files = data.split_files("train", limit=3)
    assert asked["patterns"] == names[:3]
    assert [f.split("/")[-1] for f in files] == ["train-00000-of-00028.parquet", "train-00001-of-00028.parquet",
                                                 "train-00002-of-00028.parquet"]
