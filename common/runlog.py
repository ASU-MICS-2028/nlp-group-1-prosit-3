"""Proof for every run: each printed line also goes to a log file, and the environment is recorded.

    log = RunLog(Path("eval/results/<run>/train.log"))
    log("step 10  loss 0.512")             # printed and appended (appends across resumed sessions)
    save_json(out / "environment.json", environment())
"""

import datetime
import json
import platform
import subprocess
from pathlib import Path


class RunLog:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def __call__(self, line: str) -> None:
        print(line, flush=True)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def environment() -> dict:
    """What someone needs to reproduce the run: code version, hardware, library versions, start time."""
    import torch
    import transformers

    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    except OSError:
        commit = ""
    if torch.cuda.is_available():
        device = f"cuda: {torch.cuda.get_device_name(0)} ({torch.cuda.get_device_properties(0).total_memory / 1e9:.0f} GB)"
    else:
        device = "mps" if torch.backends.mps.is_available() else "cpu"
    return {
        "git_commit": commit or "unknown",
        "device": device,
        "host": platform.node(),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "started": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    }


def save_json(path: Path, data: dict) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
