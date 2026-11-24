"""Run a trained M1 BiLSTM + CTC checkpoint on the shared 1,000-clip test set.

Example:
    uv run python -m models.rnn_ctc.predict \
        --checkpoint /content/drive/MyDrive/prosit3-m1/run1/best.pt \
        --out eval/results/m1-bilstm-ctc-run1/predictions.csv
"""

import argparse
import csv
from pathlib import Path

import torch

from common.data import fetch_test_audio, load_audio, load_test_set
from models.rnn_ctc.data import waveform_to_log_mel
from models.rnn_ctc.model import BiLSTMCTC, greedy_decode
from models.rnn_ctc.train import pick_device


def load_model(checkpoint_path: Path, device: torch.device) -> BiLSTMCTC:
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=True)
    cfg = ckpt["config"]
    model = BiLSTMCTC(
        hidden_size=cfg["hidden_size"],
        num_layers=cfg["num_layers"],
        dropout=cfg["dropout"],
        subsample=cfg["subsample"],
    ).to(device)
    model.load_state_dict(ckpt["model_state"])
    model.eval()
    return model


@torch.no_grad()
def predict_test_set(checkpoint_path: Path, out_csv: Path) -> None:
    device = pick_device()
    model = load_model(checkpoint_path, device)
    paths = fetch_test_audio()
    rows = load_test_set()

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["audio_id", "hypothesis"])
        for idx, row in enumerate(rows, start=1):
            audio = load_audio(paths[row["audio_id"]])
            features = waveform_to_log_mel(audio).unsqueeze(0).to(device)
            lengths = torch.tensor([features.shape[1]], dtype=torch.long, device=device)
            log_probs, out_lens = model(features, lengths)
            hyp = greedy_decode(log_probs, out_lens)[0]
            writer.writerow([row["audio_id"], hyp])
            if idx % 200 == 0 or idx == len(rows):
                print(f"Predicted {idx}/{len(rows)} clips")


def main() -> None:
    ap = argparse.ArgumentParser(description="Predict on common/test_set.csv with an M1 checkpoint.")
    ap.add_argument("--checkpoint", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True, help="Output predictions.csv path.")
    args = ap.parse_args()
    predict_test_set(args.checkpoint, args.out)


if __name__ == "__main__":
    main()
