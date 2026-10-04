"""The chapter examples must keep running (ch01 crashes on purpose)."""

import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLES = Path(__file__).resolve().parents[2] / "examples"


@pytest.mark.parametrize(
    "name",
    [
        "ch03_exceptions.py",
        "ch04_csv_pitfalls.py",
        "ch05_floats.py",
        "ch06_mutable_default.py",
        "ch08_logging.py",
        "ch09_profile.py",
    ],
)
def test_example_runs(name, tmp_path):
    proc = subprocess.run(
        [sys.executable, str(EXAMPLES / name)], capture_output=True, text=True, cwd=tmp_path, timeout=120
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip()


def test_ch01_crashes_with_a_keyerror_two_frames_up(tmp_path):
    proc = subprocess.run(
        [sys.executable, str(EXAMPLES / "ch01_traceback.py")], capture_output=True, text=True, cwd=tmp_path, timeout=60
    )
    assert (
        proc.returncode == 1
        and "KeyError: 'threshold'" in proc.stderr
        and "in alerts" in proc.stderr
        and "in main" in proc.stderr
    )


def test_ch02_tests_pass():
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(EXAMPLES / "ch02_first_test.py"), "-q", "-o", "addopts="],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stdout
