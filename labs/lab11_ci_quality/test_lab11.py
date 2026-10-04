"""Lab 11 check: the three CI jobs - lint (ruff), types (mypy) and tests - must all pass on quality.py.
Run with:  python -m pytest labs/lab11_ci_quality -q"""

import importlib.util
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pytest

SRC = Path(os.environ.get("ENGDEBUG_LAB_SRC", Path(__file__).parent / "buggy"))
spec = importlib.util.spec_from_file_location("quality", SRC / "quality.py")
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)


@pytest.mark.skipif(shutil.which("ruff") is None, reason="ruff not installed")
def test_lint_job_is_green():
    proc = subprocess.run(["ruff", "check", "--isolated", "--select", "E,F,W,I,B", "--line-length", "120", str(SRC / "quality.py")], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr


@pytest.mark.skipif(shutil.which("mypy") is None, reason="mypy not installed")
def test_type_job_is_green():
    proc = subprocess.run([sys.executable, "-m", "mypy", "--strict", "--no-error-summary", str(SRC / "quality.py")], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_hours_between_is_whole_hours_and_symmetric():
    a, b = datetime(2026, 3, 2, 8, 0), datetime(2026, 3, 2, 10, 45)
    assert q.hours_between(a, b) == 2 and q.hours_between(b, a) == 2
    assert isinstance(q.hours_between(a, b), int)


def test_shift_boundaries():
    assert q.shift_for(datetime(2026, 3, 2, 5, 59)) == "night"
    assert q.shift_for(datetime(2026, 3, 2, 6, 0)) == "day"
    assert q.shift_for(datetime(2026, 3, 2, 22, 0)) == "night"


def test_format_duration():
    assert q.format_duration(2.5) == "2 h 30 min" and q.format_duration(0.25) == "0 h 15 min"


def test_report_on_empty_list_does_not_crash():
    assert q.report([]) == "span: 0 h 0 min"
