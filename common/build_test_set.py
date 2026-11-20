"""Build common/test_set.csv once: 500 clinical + 500 general clips from the AfriSpeech-200 test split, seed 42.

    uv run python -m common.build_test_set

Run once and commit the CSV. Re-running gives the same file. Changing it needs a new decision record.
"""

import csv
import random

from common.data import TEST_SET, read_split

PER_DOMAIN = 500
COLUMNS = ["audio_id", "transcript", "domain", "accent", "duration"]


def main() -> None:
    rows = [r for r in read_split("test", COLUMNS) if r["transcript"].strip()]
    rng = random.Random(42)
    chosen = []
    for domain in ["clinical", "general"]:
        pool = sorted((r for r in rows if r["domain"] == domain), key=lambda r: r["audio_id"])
        chosen += rng.sample(pool, PER_DOMAIN)
    chosen.sort(key=lambda r: r["audio_id"])
    with open(TEST_SET, "w", newline="") as f:
        w = csv.DictWriter(f, COLUMNS)
        w.writeheader()
        for r in chosen:
            w.writerow({**r, "transcript": " ".join(r["transcript"].split()), "duration": round(r["duration"], 3)})
    print(f"wrote {len(chosen)} rows to {TEST_SET}")


if __name__ == "__main__":
    main()
