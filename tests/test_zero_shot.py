from pathlib import Path

from models.whisper_full.zero_shot import run_dir


def test_hub_model_goes_to_a_zeroshot_folder():
    assert run_dir("openai/whisper-small", fallback=True) == Path("eval/results/m3-whisper-small-zeroshot-fallback")
    assert run_dir("openai/whisper-small", fallback=False) == Path("eval/results/m3-whisper-small-zeroshot")


def test_fine_tuned_checkpoint_goes_next_to_its_training_logs(tmp_path):
    best = tmp_path / "checkpoints" / "whisper-small-afrispeech" / "best"
    best.mkdir(parents=True)
    assert run_dir(str(best), fallback=True) == Path("eval/results/m3-whisper-small-afrispeech")


def test_language_detection_run_gets_its_own_folder():
    assert run_dir("openai/whisper-small", fallback=True, detect=True) == Path(
        "eval/results/m3-whisper-small-zeroshot-fallback-detect")


def test_generate_kwargs_force_english_unless_detecting():
    from models.whisper_full.zero_shot import generate_kwargs
    assert generate_kwargs(fallback=False, detect=False) == {"language": "en", "task": "transcribe"}
    assert "language" not in generate_kwargs(fallback=False, detect=True)
    assert generate_kwargs(fallback=True, detect=True)["compression_ratio_threshold"] == 1.35
