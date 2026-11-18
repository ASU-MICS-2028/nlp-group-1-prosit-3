"""Regenerate every folder index (README.md) from the files' frontmatter.

    python3 scripts/build_indexes.py           # rewrite the indexes
    python3 scripts/build_indexes.py --check   # exit 1 if any index is stale (hook and CI)

Everything above the `<!-- index -->` line in a README is kept; everything below is replaced.
Nobody edits below that line by hand, so parallel PRs never fight over an index.
"""

import argparse
import re
import sys
from pathlib import Path

MARKER = "<!-- index -->"
# folder, which files, extra columns after the linked title
FOLDERS = [
    ("knowledge", "*.md", ["tags", "author"]),
    ("knowledge/sources", "*.md", ["source"]),
    ("learnings", "*.md", ["tags", "author"]),
    ("docs/decisions", "[0-9]*.md", ["status", "date"]),
    ("docs/changes", "*.md", ["owner", "issue", "ai-use"]),
    ("docs/plans", "*.md", ["owner", "issue", "status"]),
    ("eval/results", "*/run.md", ["model", "owner", "wer"]),
]


def read_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text().splitlines()
    if not lines or lines[0].strip() != "---" or "---" not in [l.strip() for l in lines[1:]]:
        raise ValueError(f"{path}: no frontmatter (the file must start with a --- block)")
    end = [l.strip() for l in lines[1:]].index("---") + 1
    meta = {}
    for line in lines[1:end]:
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"')
    if not meta.get("title"):
        raise ValueError(f"{path}: frontmatter has no title")
    return meta


def table(folder: Path, pattern: str, columns: list[str]) -> str:
    files = sorted(p for p in folder.glob(pattern) if p.name != "README.md" and not p.name.startswith("TEMPLATE"))
    cell = lambda s: s.replace("|", "\\|")
    rows = ["| Title | " + " | ".join(columns) + " |", "|---" * (len(columns) + 1) + "|"]
    for p in files:
        meta = read_frontmatter(p)
        link = f"[{cell(meta['title'])}]({p.relative_to(folder).as_posix()})"
        rows.append("| " + " | ".join([link] + [cell(meta.get(c, "")) for c in columns]) + " |")
    return "\n".join(rows) + "\n"


def check_decision_numbers(folder: Path) -> None:
    seen = {}
    for p in sorted(folder.glob("[0-9]*.md")):
        number = re.match(r"\d+", p.name).group()
        if number in seen:
            raise ValueError(f"decision number {number} used twice: {seen[number].name} and {p.name}; renumber the newer one")
        seen[number] = p


def build(root: Path) -> dict[Path, str]:
    out = {}
    for name, pattern, columns in FOLDERS:
        readme = root / name / "README.md"
        if not readme.exists():
            continue
        if name == "docs/decisions":
            check_decision_numbers(root / name)
        text = readme.read_text()
        if MARKER not in text:
            raise ValueError(f"{readme}: missing the {MARKER} line")
        out[readme] = text.split(MARKER)[0] + MARKER + "\n\n" + table(root / name, pattern, columns)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = ap.parse_args(argv)
    try:
        new = build(args.root)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1
    stale = [p for p, text in new.items() if p.read_text() != text]
    if args.check:
        for p in stale:
            print(f"stale index: {p} (run python3 scripts/build_indexes.py)", file=sys.stderr)
        return 1 if stale else 0
    for p in stale:
        p.write_text(new[p])
    return 0


if __name__ == "__main__":
    sys.exit(main())
