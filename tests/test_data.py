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
