import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_secrets.py"


def run_on(tmp_path, files):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    for name, text in files.items():
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        subprocess.run(["git", "add", "-f", name], cwd=tmp_path, check=True)
    return subprocess.run([sys.executable, str(SCRIPT), "--staged"], cwd=tmp_path, capture_output=True, text=True)


def test_blocks_env(tmp_path):
    r = run_on(tmp_path, {".env": "HF_TOKEN=x\n"})
    assert r.returncode == 1 and ".env" in r.stderr


def test_blocks_audio_and_models(tmp_path):
    for name in ["a.wav", "x.safetensors", "data/clip.flac", "audio.tar.gz", "w.pt", "m.bin", "c.ckpt"]:
        d = tmp_path / name.replace("/", "_").replace(".", "_")
        d.mkdir()
        r = run_on(d, {name: "x"})
        assert r.returncode == 1, name


def test_blocks_hf_token(tmp_path):
    r = run_on(tmp_path, {"notes.md": "token hf_" + "a" * 34 + "\n"})
    assert r.returncode == 1 and "notes.md:1" in r.stderr


def test_allows_csv(tmp_path):
    r = run_on(tmp_path, {"common/test_set.csv": "audio_id,transcript\n1,the patient has fever\n"})
    assert r.returncode == 0, r.stderr


def test_allows_code_under_models(tmp_path):
    r = run_on(tmp_path, {"models/rnn_ctc/train.py": "print('hi')\n"})
    assert r.returncode == 0, r.stderr


def test_blocks_more_audio_and_data_formats(tmp_path):
    for name in ["A.WAV", "note.webm", "c.ogg", "d.m4a", "f.npy", "g.parquet", "h.zip", "k.tgz", "j.pkl"]:
        d = tmp_path / name.replace(".", "_")
        d.mkdir()
        r = run_on(d, {name: "x"})
        assert r.returncode == 1, name


def test_blocks_rename_into_data(tmp_path):
    run_on(tmp_path, {"note.txt": "x"})
    subprocess.run(["git", "commit", "-qm", "x", "--no-verify"], cwd=tmp_path, check=True,
                   env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t", "PATH": "/usr/bin:/bin"})
    (tmp_path / "data").mkdir()
    subprocess.run(["git", "mv", "-f", "note.txt", "data/clip.txt"], cwd=tmp_path, check=True)
    r = subprocess.run([sys.executable, str(SCRIPT), "--staged"], cwd=tmp_path, capture_output=True, text=True)
    assert r.returncode == 1 and "data/clip.txt" in r.stderr
