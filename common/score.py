"""Score one model's predictions on the fixed test set. Every model uses this, so numbers are comparable.

    uv run python -m common.score eval/results/<run>/predictions.csv

predictions.csv has two columns, `audio_id,hypothesis`, with every test-set ID exactly once.
Writes scores.json next to it: WER and CER overall, by domain, and by accent (accents with 30+ clips).
"""

import csv
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import jiwer

TEST_SET = Path(__file__).with_name("test_set.csv")
MIN_ACCENT_CLIPS = 30  # smaller accents give noisy WER (decision 0009)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).replace("\u2019", "'").replace("\u2018", "'").replace("\u02bc", "'")
    text = re.sub(r"[^\w' ]|_", " ", text.lower())  # keep letters, digits, apostrophes
    text = " ".join(text.split())
    return re.sub(r"(\d) s\b", r"\1s", text)  # AfriSpeech writes "50s" as "50 s"


def _wer_cer(refs: list[str], hyps: list[str]) -> dict:
    # corpus level: total errors / total reference words, not an average of per-clip WERs
    return {"wer": round(jiwer.wer(refs, hyps), 4), "cer": round(jiwer.cer(refs, hyps), 4), "n": len(refs)}


def score(predictions_csv: Path, test_csv: Path = TEST_SET) -> dict:
    with open(test_csv, newline="", encoding="utf-8") as f:
        test = {row["audio_id"]: row for row in csv.DictReader(f)}
    with open(predictions_csv, newline="", encoding="utf-8-sig") as f:  # -sig: Excel's "CSV UTF-8" adds a BOM
        reader = csv.DictReader(f)
        if not {"audio_id", "hypothesis"} <= set(reader.fieldnames or []):
            raise ValueError(f"{predictions_csv} needs columns audio_id,hypothesis; found {reader.fieldnames}")
        preds = list(reader)

    ids = [p["audio_id"] for p in preds]
    duplicates = sorted(i for i, n in Counter(ids).items() if n > 1)
    missing = sorted(test.keys() - set(ids))
    extra = sorted(set(ids) - test.keys())
    if duplicates or missing or extra:
        raise ValueError(f"{predictions_csv} does not match the test set: "
                         f"duplicates={duplicates[:20]} missing={missing[:20]} extra={extra[:20]} "
                         f"(counts {len(duplicates)}/{len(missing)}/{len(extra)})")

    groups = {"overall": {"all": ([], [])}, "domain": {}, "accent": {}}
    for p in preds:
        row = test[p["audio_id"]]
        ref, hyp = normalize(row["transcript"]), normalize(p["hypothesis"] or "")
        for kind, key in [("overall", "all"), ("domain", row["domain"]), ("accent", row["accent"])]:
            refs, hyps = groups[kind].setdefault(key, ([], []))
            refs.append(ref)
            hyps.append(hyp)

    return {
        "overall": _wer_cer(*groups["overall"]["all"]),
        "domain": {k: _wer_cer(*v) for k, v in sorted(groups["domain"].items())},
        "accent": {k: _wer_cer(*v) for k, v in sorted(groups["accent"].items()) if len(v[0]) >= MIN_ACCENT_CLIPS},
    }


def main() -> None:
    predictions = Path(sys.argv[1])
    result = score(predictions)
    (predictions.parent / "scores.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"overall  WER {result['overall']['wer']:.3f}  CER {result['overall']['cer']:.3f}  n={result['overall']['n']}")
    for kind in ["domain", "accent"]:
        for name, s in result[kind].items():
            print(f"{kind:7}  {name:20} WER {s['wer']:.3f}  CER {s['cer']:.3f}  n={s['n']}")


if __name__ == "__main__":
    main()
