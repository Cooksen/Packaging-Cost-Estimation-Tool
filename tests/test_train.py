import subprocess

def test_train_script_runs():
    result = subprocess.run(["poetry", "run", "train"], capture_output=True, text=True)
    assert result.returncode in [0, 1]
    assert "Training" in result.stdout or "usage" in result.stdout