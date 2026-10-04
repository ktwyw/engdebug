"""Lab 12 check: delegates to the capstone acceptance tests (buggy = capstone/release, solution = solutions/capstone)."""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = os.environ.get("ENGDEBUG_LAB_SRC")


def test_capstone_acceptance():
    env = dict(os.environ)
    env["ENGDEBUG_CAPSTONE_SRC"] = SRC if SRC else str(ROOT / "capstone" / "release")
    proc = subprocess.run([sys.executable, "-m", "pytest", str(ROOT / "capstone" / "tests"), "-q", "--tb=short", "-p", "no:cacheprovider"], capture_output=True, text=True, env=env, cwd=ROOT, timeout=900)
    assert proc.returncode == 0, proc.stdout[-2000:]
