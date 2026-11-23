from pathlib import Path

from models.whisper_full.zero_shot import run_dir


def test_hub_model_goes_to_a_zeroshot_folder():
    assert run_dir("openai/whisper-small", fallback=True) == Path("eval/results/m3-whisper-small-zeroshot-fallback")
    assert run_dir("openai/whisper-small", fallback=False) == Path("eval/results/m3-whisper-small-zeroshot")


def test_fine_tuned_checkpoint_goes_next_to_its_training_logs(tmp_path):
    best = tmp_path / "checkpoints" / "whisper-small-afrispeech" / "best"
    best.mkdir(parents=True)
    assert run_dir(str(best), fallback=True) == Path("eval/results/m3-whisper-small-afrispeech")
