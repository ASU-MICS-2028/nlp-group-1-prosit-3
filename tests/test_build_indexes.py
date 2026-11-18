import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_indexes as bi  # noqa: E402


def note(path, title, extra=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\ntitle: {title}\n{extra}---\n\nBody.\n")


def setup_knowledge(root):
    (root / "knowledge").mkdir(parents=True)
    (root / "knowledge" / "README.md").write_text("# Knowledge\n\nIntro stays.\n\n<!-- index -->\nold table\n")
    note(root / "knowledge" / "b-note.md", "B title", "tags: [asr]\nauthor: Ann\n")
    note(root / "knowledge" / "a-note.md", "A title", "tags: [rnn]\nauthor: Bo\n")


def test_index_lists_notes_sorted(tmp_path):
    setup_knowledge(tmp_path)
    text = bi.build(tmp_path)[tmp_path / "knowledge" / "README.md"]
    assert "[A title](a-note.md)" in text and "[B title](b-note.md)" in text
    assert text.index("a-note.md") < text.index("b-note.md")
    assert "old table" not in text


def test_keeps_text_above_marker(tmp_path):
    setup_knowledge(tmp_path)
    text = bi.build(tmp_path)[tmp_path / "knowledge" / "README.md"]
    assert text.startswith("# Knowledge\n\nIntro stays.\n\n<!-- index -->\n")


def test_missing_title_names_file(tmp_path):
    setup_knowledge(tmp_path)
    (tmp_path / "knowledge" / "bad.md").write_text("no frontmatter here\n")
    with pytest.raises(ValueError, match="bad.md"):
        bi.build(tmp_path)


def test_duplicate_decision_number(tmp_path):
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True)
    (d / "README.md").write_text("# Decisions\n\n<!-- index -->\n")
    note(d / "0003-a.md", "A", "status: Accepted\ndate: 2026-11-18\n")
    note(d / "0003-b.md", "B", "status: Accepted\ndate: 2026-11-18\n")
    with pytest.raises(ValueError, match=r"0003-a\.md.*0003-b\.md"):
        bi.build(tmp_path)


def test_check_detects_stale(tmp_path):
    setup_knowledge(tmp_path)
    assert bi.main(["--root", str(tmp_path)]) == 0
    assert bi.main(["--check", "--root", str(tmp_path)]) == 0
    note(tmp_path / "knowledge" / "c-note.md", "C title")
    assert bi.main(["--check", "--root", str(tmp_path)]) == 1
