from models.whisper_full.finetune import pad_labels


def test_pad_labels_uses_minus_100_so_padding_is_ignored_by_the_loss():
    out = pad_labels([[5, 6, 7], [8]])
    assert out.tolist() == [[5, 6, 7], [8, -100, -100]]


def test_pad_labels_drops_the_start_token_the_model_adds_itself():
    sot = 50258
    out = pad_labels([[sot, 5, 6], [sot, 7]], start_token=sot)
    assert out.tolist() == [[5, 6], [7, -100]]


def tiny_whisper():
    from transformers import WhisperConfig, WhisperForConditionalGeneration
    cfg = WhisperConfig(vocab_size=64, d_model=8, encoder_layers=1, decoder_layers=1, encoder_attention_heads=1,
                        decoder_attention_heads=1, encoder_ffn_dim=8, decoder_ffn_dim=8, max_source_positions=8,
                        max_target_positions=8, num_mel_bins=4, pad_token_id=0, bos_token_id=1, eos_token_id=2,
                        decoder_start_token_id=1)
    return WhisperForConditionalGeneration(cfg)


def test_resume_restores_step_best_weights_and_optimizer(tmp_path):
    import torch
    from models.whisper_full.finetune import load_state, save_state

    model = tiny_whisper()
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: 1.0)
    scaler = torch.amp.GradScaler(enabled=False)
    model(input_features=torch.randn(1, 4, 16), labels=torch.tensor([[3, 4]])).loss.backward()
    opt.step(); sched.step()
    save_state(tmp_path / "last", model, opt, sched, scaler, step=500, best=0.31)

    model2 = tiny_whisper()
    opt2 = torch.optim.AdamW(model2.parameters(), lr=1e-3)
    sched2 = torch.optim.lr_scheduler.LambdaLR(opt2, lambda s: 1.0)
    step, best = load_state(tmp_path / "last", model2, opt2, sched2, torch.amp.GradScaler(enabled=False))
    assert (step, best) == (500, 0.31)
    assert all(torch.equal(a, b) for a, b in zip(model.state_dict().values(), model2.state_dict().values()))
    assert opt2.state_dict()["state"].keys() == opt.state_dict()["state"].keys()
    assert sched2.last_epoch == sched.last_epoch


def test_load_state_without_a_saved_run_starts_fresh(tmp_path):
    from models.whisper_full.finetune import load_state
    assert load_state(tmp_path / "nothing", None, None, None, None) == (0, float("inf"))
