"""BiLSTM + CTC acoustic model and greedy CTC decoder."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

from models.rnn_ctc.data import BLANK_IDX, N_MELS, VOCAB, ids_to_text


def _conv2d_out_len(lengths: torch.Tensor, kernel: int = 3, stride: int = 2, padding: int = 1) -> torch.Tensor:
    return torch.div(lengths + 2 * padding - kernel, stride, rounding_mode="floor") + 1


class BiLSTMCTC(nn.Module):
    """Stacked Bidirectional LSTM acoustic model trained with CTC loss.

    Input:  padded log-mel spectrograms of shape (batch, time, n_mels) and frame lengths (batch,)
    Output: log probabilities of shape (time_out, batch, vocab_size) and output lengths (batch,)
    """

    def __init__(
        self,
        n_mels: int = N_MELS,
        vocab_size: int = len(VOCAB),
        hidden_size: int = 256,
        num_layers: int = 3,
        dropout: float = 0.2,
        subsample: bool = False,
    ) -> None:
        super().__init__()
        self.n_mels = n_mels
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.dropout_p = dropout
        self.subsample = subsample

        if subsample:
            # Two stride-2 conv layers downsample time and frequency by 4x (80 mel -> 20).
            self.conv = nn.Sequential(
                nn.Conv2d(1, 32, kernel_size=3, stride=2, padding=1),
                nn.ReLU(),
                nn.Conv2d(32, 32, kernel_size=3, stride=2, padding=1),
                nn.ReLU(),
            )
            freq_out = ((n_mels + 2 - 3) // 2 + 1 + 2 - 3) // 2 + 1
            rnn_input_size = 32 * freq_out
        else:
            self.conv = None
            rnn_input_size = n_mels

        self.rnn = nn.LSTM(
            input_size=rnn_input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.head = nn.Linear(hidden_size * 2, vocab_size)

    def output_lengths(self, input_lengths: torch.Tensor) -> torch.Tensor:
        if not self.subsample:
            return input_lengths
        return _conv2d_out_len(_conv2d_out_len(input_lengths))

    def forward(
        self, features: torch.Tensor, feature_lengths: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        x = features
        lengths = self.output_lengths(feature_lengths)

        if self.conv is not None:
            # (batch, 1, time, freq) -> (batch, 32, time/4, freq/4) -> (batch, time/4, 32*freq/4)
            x = self.conv(x.unsqueeze(1))
            b, c, t, f = x.shape
            x = x.permute(0, 2, 1, 3).reshape(b, t, c * f)

        packed = pack_padded_sequence(x, lengths.cpu(), batch_first=True, enforce_sorted=False)
        packed_out, _ = self.rnn(packed)
        out, _ = pad_packed_sequence(packed_out, batch_first=True)
        logits = self.head(out)
        log_probs = F.log_softmax(logits, dim=-1).transpose(0, 1)  # (time, batch, vocab)
        return log_probs, lengths


def greedy_decode(log_probs: torch.Tensor, lengths: torch.Tensor) -> list[str]:
    """CTC greedy decoding: argmax per frame, merge consecutive repeats, drop blanks."""
    preds = log_probs.argmax(dim=-1).transpose(0, 1).cpu().tolist()  # (batch, time)
    length_list = lengths.cpu().tolist()
    texts: list[str] = []
    for seq, seq_len in zip(preds, length_list):
        collapsed: list[int] = []
        prev = BLANK_IDX
        for token_id in seq[:seq_len]:
            if token_id != prev and token_id != BLANK_IDX:
                collapsed.append(token_id)
            prev = token_id
        texts.append(ids_to_text(collapsed))
    return texts
