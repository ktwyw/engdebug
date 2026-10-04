"""Lab 01 check: every script must run without error and print the expected result.
Run with:  python -m pytest labs/lab01_tracebacks -q
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

SRC = Path(os.environ.get("ENGDEBUG_LAB_SRC", Path(__file__).parent / "buggy"))

EXPECTED = {
    "script1_syntax.py": "mean temperature: 71.78 degC",
    "script2_name.py": "[610.0, 630.0, 590.0]",
    "script3_type.py": "1 alert(s): [125.4]",
    "script4_index.py": "[0.8, -1.2, 2.3]",
    "script5_attribute_key.py": "T101: 71.2 DEGC",
}


@pytest.mark.parametrize("script, expected", EXPECTED.items())
def test_script_runs_and_prints(script, expected):
    proc = subprocess.run([sys.executable, str(SRC / script)], capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0, f"{script} failed:\n{proc.stderr}"
    out = proc.stdout.strip().splitlines()[-1]
    assert out == expected or _close(out, expected), f"{script} printed {out!r}, expected {expected!r}"


def _close(out, expected):
    """Allow floating-point noise in script 4's differences."""
    try:
        a = [float(x) for x in out.strip("[]").split(",")]
        b = [float(x) for x in expected.strip("[]").split(",")]
        return len(a) == len(b) and all(abs(x - y) < 1e-9 for x, y in zip(a, b))
    except ValueError:
        return False
