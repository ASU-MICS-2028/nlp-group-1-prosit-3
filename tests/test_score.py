import csv

import pytest

from common.score import normalize, score

FIELDS = ["audio_id", "transcript", "domain", "accent", "duration"]


def write_test_set(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for i, (text, domain, accent) in enumerate(rows):
            w.writerow({"audio_id": f"a{i}", "transcript": text, "domain": domain, "accent": accent, "duration": 3.0})
    return path


def write_predictions(path, pairs):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["audio_id", "hypothesis"])
        w.writerows(pairs)
    return path


def test_normalize():
    assert normalize("His mother is in her 50 s .") == "his mother is in her 50s"
    assert normalize("  B.P.  was HIGH!! ") == "b p was high"


def test_normalize_unicode():
    assert normalize("The patient\u2019s chart") == normalize("the patient's chart") == "the patient's chart"
    assert normalize("cafe\u0301") == normalize("caf\u00e9")


def test_reads_excel_bom(tmp_path):
    test = write_test_set(tmp_path / "t.csv", [("fever", "clinical", "yoruba")])
    preds = tmp_path / "p.csv"
    preds.write_text("audio_id,hypothesis\na0,fever\n", encoding="utf-8-sig")
    assert score(preds, test)["overall"]["wer"] == 0.0


def test_missing_hypothesis_column_is_explained(tmp_path):
    test = write_test_set(tmp_path / "t.csv", [("fever", "clinical", "yoruba")])
    preds = tmp_path / "p.csv"
    preds.write_text("audio_id,text\na0,fever\n")
    with pytest.raises(ValueError, match="audio_id,hypothesis"):
        score(preds, test)


def test_perfect_score(tmp_path):
    t = write_test_set(tmp_path / "t.csv", [("The patient has fever .", "clinical", "yoruba")])
    p = write_predictions(tmp_path / "p.csv", [("a0", "the patient has fever")])
    s = score(p, t)
    assert s["overall"]["wer"] == 0.0 and s["overall"]["cer"] == 0.0 and s["overall"]["n"] == 1


def test_known_wer(tmp_path):
    t = write_test_set(tmp_path / "t.csv", [("the patient has fever", "clinical", "igbo")])
    p = write_predictions(tmp_path / "p.csv", [("a0", "the patient fever")])
    assert score(p, t)["overall"]["wer"] == 0.25


def test_empty_hypothesis(tmp_path):
    t = write_test_set(tmp_path / "t.csv", [("the patient has fever", "clinical", "igbo")])
    p = write_predictions(tmp_path / "p.csv", [("a0", "")])
    assert score(p, t)["overall"]["wer"] == 1.0


def test_by_domain(tmp_path):
    t = write_test_set(tmp_path / "t.csv", [("take two tablets", "clinical", "hausa"), ("the market is busy", "general", "twi")])
    p = write_predictions(tmp_path / "p.csv", [("a0", "take two tablets"), ("a1", "the market busy")])
    d = score(p, t)["domain"]
    assert d["clinical"]["n"] == 1 and d["general"]["n"] == 1
    assert d["clinical"]["wer"] == 0.0 and d["general"]["wer"] == 0.25


def test_missing_ids_refused(tmp_path):
    t = write_test_set(tmp_path / "t.csv", [("a b", "clinical", "x"), ("c d", "general", "x")])
    p = write_predictions(tmp_path / "p.csv", [("a0", "a b")])
    with pytest.raises(ValueError, match="a1"):
        score(p, t)


def test_duplicate_or_extra_ids_refused(tmp_path):
    t = write_test_set(tmp_path / "t.csv", [("a b", "clinical", "x")])
    dup = write_predictions(tmp_path / "dup.csv", [("a0", "a b"), ("a0", "a b")])
    with pytest.raises(ValueError, match="a0"):
        score(dup, t)
    extra = write_predictions(tmp_path / "extra.csv", [("a0", "a b"), ("zz9", "x")])
    with pytest.raises(ValueError, match="zz9"):
        score(extra, t)


def test_small_accent_dropped(tmp_path):
    rows = [("one two", "clinical", "yoruba")] * 30 + [("one two", "general", "gerawa")] * 3
    t = write_test_set(tmp_path / "t.csv", rows)
    p = write_predictions(tmp_path / "p.csv", [(f"a{i}", "one two") for i in range(33)])
    acc = score(p, t)["accent"]
    assert "yoruba" in acc and acc["yoruba"]["n"] == 30
    assert "gerawa" not in acc
