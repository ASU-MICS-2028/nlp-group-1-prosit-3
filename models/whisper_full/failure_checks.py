"""Count the two zero-shot failure types in one or more predictions files (one row each):
- loops: clips whose WER is above 1 (more wrong words than reference words, usually a repeated phrase)
- spoken punctuation: hypotheses saying "comma", "full stop" etc. when the reference does not

    uv run python -m models.whisper_full.failure_checks eval/results/<run>/predictions.csv [...]
"""

import csv
import re
import sys

import jiwer

from common.data import load_test_set
from common.score import normalize

PUNCT = re.compile(r"\b(comma|full stop|period|new line|new paragraph|colon|semicolon|question mark)\b")


def count(predictions_csv: str) -> tuple[int, int]:
    refs = {r["audio_id"]: normalize(r["transcript"]) for r in load_test_set()}
    loops = punct = 0
    with open(predictions_csv, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            ref, hyp = refs[row["audio_id"]], normalize(row["hypothesis"])
            loops += bool(ref) and jiwer.wer(ref, hyp) > 1
            punct += bool(PUNCT.search(hyp)) and not PUNCT.search(ref)
    return loops, punct


if __name__ == "__main__":
    print("predictions,clips_wer_over_1,spoken_punctuation_not_in_reference")
    for path in sys.argv[1:]:
        print(path, *count(path), sep=",")
