import json

from common.runlog import RunLog, environment


def test_runlog_prints_and_keeps_every_line(tmp_path, capsys):
    log = RunLog(tmp_path / "run" / "train.log")
    log("step 10  loss 0.5")
    log("step 20  loss 0.4")
    assert capsys.readouterr().out == "step 10  loss 0.5\nstep 20  loss 0.4\n"
    assert (tmp_path / "run" / "train.log").read_text().splitlines() == ["step 10  loss 0.5", "step 20  loss 0.4"]


def test_runlog_appends_across_sessions(tmp_path):
    path = tmp_path / "train.log"
    RunLog(path)("first session")
    RunLog(path)("resumed")
    assert path.read_text().splitlines() == ["first session", "resumed"]


def test_environment_records_what_reproduces_a_run():
    env = environment()
    assert {"git_commit", "device", "python", "torch", "transformers", "started"} <= env.keys()
    json.dumps(env)  # must be saveable as JSON
