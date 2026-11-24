"""Train the M1 BiLSTM + CTC baseline on AfriSpeech-200.

Example (Colab Pro L4/A100):
    uv run python -m models.rnn_ctc.train \
        --out-dir /content/drive/MyDrive/prosit3-m1/run1 \
        --epochs 20 --batch-size 32 --hidden-size 256 --num-layers 3 --subsample --spec-augment

Example (local CPU overfit sanity check on 8 clips):
    uv run python -m models.rnn_ctc.train \
        --out-dir checkpoints/overfit-check \
        --max-train-clips 8 --max-dev-clips 8 --epochs 40 --batch-size 4 --lr 3e-3
"""

import argparse
import json
import time
from pathlib import Path

import jiwer
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from models.rnn_ctc.data import AfriSpeechCTCDataset, BLANK_IDX, collate_ctc_batch
from models.rnn_ctc.model import BiLSTMCTC, greedy_decode


def pick_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


@torch.no_grad()
def evaluate(model: BiLSTMCTC, loader: DataLoader, criterion: nn.CTCLoss, device: torch.device) -> dict:
    model.eval()
    total_loss = 0.0
    batches = 0
    refs: list[str] = []
    hyps: list[str] = []

    for batch in loader:
        features = batch["features"].to(device)
        feat_lens = batch["feature_lengths"].to(device)
        targets = batch["targets"].to(device)
        target_lens = batch["target_lengths"].to(device)

        log_probs, out_lens = model(features, feat_lens)
        loss = criterion(log_probs, targets, out_lens, target_lens)
        total_loss += float(loss.item())
        batches += 1

        refs.extend(batch["transcripts"])
        hyps.extend(greedy_decode(log_probs, out_lens))

    return {
        "loss": round(total_loss / max(1, batches), 4),
        "wer": round(jiwer.wer(refs, hyps), 4),
        "cer": round(jiwer.cer(refs, hyps), 4),
        "sample_ref": refs[0] if refs else "",
        "sample_hyp": hyps[0] if hyps else "",
    }


def save_checkpoint(
    path: Path,
    model: BiLSTMCTC,
    optimizer: torch.optim.Optimizer,
    epoch: int,
    best_wer: float,
    config: dict,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "epoch": epoch,
            "best_wer": best_wer,
            "config": config,
            "model_state": model.state_dict(),
            "optimizer_state": optimizer.state_dict(),
        },
        path,
    )


def train(args: argparse.Namespace) -> None:
    torch.manual_seed(args.seed)
    device = pick_device()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    subsample_factor = 4 if args.subsample else 1
    print(f"Device: {device} | Loading AfriSpeech-200 train/dev splits...")
    train_ds = AfriSpeechCTCDataset(
        split="train",
        max_clips=args.max_train_clips,
        max_duration_s=args.max_duration,
        subsample_factor=subsample_factor,
        augment=args.spec_augment,
    )
    dev_ds = AfriSpeechCTCDataset(
        split="dev",
        max_clips=args.max_dev_clips,
        max_duration_s=args.max_duration,
        subsample_factor=subsample_factor,
        augment=False,
    )
    print(f"Loaded {len(train_ds)} train clips and {len(dev_ds)} dev clips.")

    train_loader = DataLoader(
        train_ds,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        collate_fn=collate_ctc_batch,
        pin_memory=(device.type == "cuda"),
    )
    dev_loader = DataLoader(
        dev_ds,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        collate_fn=collate_ctc_batch,
        pin_memory=(device.type == "cuda"),
    )

    config = {
        "hidden_size": args.hidden_size,
        "num_layers": args.num_layers,
        "dropout": args.dropout,
        "subsample": args.subsample,
        "spec_augment": args.spec_augment,
        "lr": args.lr,
        "batch_size": args.batch_size,
        "max_duration": args.max_duration,
    }
    model = BiLSTMCTC(
        hidden_size=args.hidden_size,
        num_layers=args.num_layers,
        dropout=args.dropout,
        subsample=args.subsample,
    ).to(device)
    param_count = sum(p.numel() for p in model.parameters())
    print(f"BiLSTMCTC parameters: {param_count:,}")

    criterion = nn.CTCLoss(blank=BLANK_IDX, zero_infinity=True)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=2)

    start_epoch = 1
    best_wer = float("inf")
    last_ckpt = out_dir / "last.pt"
    if args.resume and last_ckpt.exists():
        state = torch.load(last_ckpt, map_location=device, weights_only=True)
        model.load_state_dict(state["model_state"])
        optimizer.load_state_dict(state["optimizer_state"])
        start_epoch = int(state["epoch"]) + 1
        best_wer = float(state["best_wer"])
        print(f"Resumed from {last_ckpt} at epoch {start_epoch} (best dev WER {best_wer:.4f})")

    history: list[dict] = []
    use_amp = device.type == "cuda"
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)

    for epoch in range(start_epoch, args.epochs + 1):
        t0 = time.time()
        model.train()
        running_loss = 0.0
        batches = 0

        for batch in train_loader:
            features = batch["features"].to(device)
            feat_lens = batch["feature_lengths"].to(device)
            targets = batch["targets"].to(device)
            target_lens = batch["target_lengths"].to(device)

            optimizer.zero_grad(set_to_none=True)
            with torch.amp.autocast("cuda", enabled=use_amp):
                log_probs, out_lens = model(features, feat_lens)
                # CTCLoss is most stable in float32.
                loss = criterion(log_probs.float(), targets, out_lens, target_lens)

            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=args.grad_clip)
            scaler.step(optimizer)
            scaler.update()

            running_loss += float(loss.item())
            batches += 1

        train_loss = round(running_loss / max(1, batches), 4)
        dev_metrics = evaluate(model, dev_loader, criterion, device)
        scheduler.step(dev_metrics["loss"])
        elapsed = round(time.time() - t0, 1)

        row = {
            "epoch": epoch,
            "train_loss": train_loss,
            "dev_loss": dev_metrics["loss"],
            "dev_wer": dev_metrics["wer"],
            "dev_cer": dev_metrics["cer"],
            "lr": optimizer.param_groups[0]["lr"],
            "seconds": elapsed,
        }
        history.append(row)
        print(
            f"Epoch {epoch:02d}/{args.epochs} | train_loss={train_loss:.4f} | "
            f"dev_loss={dev_metrics['loss']:.4f} | dev_WER={dev_metrics['wer']:.4f} | "
            f"dev_CER={dev_metrics['cer']:.4f} | {elapsed:.1f}s"
        )
        print(f"  ref: {dev_metrics['sample_ref']}")
        print(f"  hyp: {dev_metrics['sample_hyp']}")

        save_checkpoint(last_ckpt, model, optimizer, epoch, best_wer, config)
        if dev_metrics["wer"] < best_wer:
            best_wer = dev_metrics["wer"]
            save_checkpoint(out_dir / "best.pt", model, optimizer, epoch, best_wer, config)

        (out_dir / "history.json").write_text(json.dumps(history, indent=2) + "\n")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Train M1 BiLSTM + CTC on AfriSpeech-200.")
    ap.add_argument("--out-dir", type=str, required=True, help="Directory for checkpoints and history (off-repo).")
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--hidden-size", type=int, default=256)
    ap.add_argument("--num-layers", type=int, default=3)
    ap.add_argument("--dropout", type=float, default=0.2)
    ap.add_argument("--grad-clip", type=float, default=5.0)
    ap.add_argument("--max-duration", type=float, default=20.0)
    ap.add_argument("--subsample", action="store_true", help="Enable 2-layer strided Conv2d 4x time subsampling.")
    ap.add_argument("--spec-augment", action="store_true", help="Enable SpecAugment during training.")
    ap.add_argument("--max-train-clips", type=int, default=None, help="Limit train clips (for smoke/overfit checks).")
    ap.add_argument("--max-dev-clips", type=int, default=None, help="Limit dev clips (for smoke/overfit checks).")
    ap.add_argument("--num-workers", type=int, default=2)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--resume", action="store_true", help="Resume from <out-dir>/last.pt if present.")
    return ap.parse_args()


if __name__ == "__main__":
    train(parse_args())
