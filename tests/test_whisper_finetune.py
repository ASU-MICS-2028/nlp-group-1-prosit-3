from models.whisper_full.finetune import pad_labels


def test_pad_labels_uses_minus_100_so_padding_is_ignored_by_the_loss():
    out = pad_labels([[5, 6, 7], [8]])
    assert out.tolist() == [[5, 6, 7], [8, -100, -100]]


def test_pad_labels_drops_the_start_token_the_model_adds_itself():
    sot = 50258
    out = pad_labels([[sot, 5, 6], [sot, 7]], start_token=sot)
    assert out.tolist() == [[5, 6], [7, -100]]
