"""Lab 13 check.  Run with:  python -m pytest labs/lab13_environment -q"""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

SRC = Path(os.environ.get("ENGDEBUG_LAB_SRC", Path(__file__).parent / "buggy"))
ROOT = Path(__file__).resolve().parents[2]


def load_module():
    spec = importlib.util.spec_from_file_location("calibrate", SRC / "calibrate.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_without_optional_dependency():
    """The module must import even when PyYAML is not installed (it is not a declared dependency)."""
    code = "import sys, builtins; real = builtins.__import__\n" "def fake(name, *a, **k):\n    if name == 'yaml': raise ModuleNotFoundError(\"No module named 'yaml'\")\n    return real(name, *a, **k)\n" "builtins.__import__ = fake\n" f"sys.path.insert(0, {str(SRC)!r}); import calibrate; print('imported')"
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0 and "imported" in proc.stdout, proc.stderr


def test_calibration_table_found_from_any_working_directory(tmp_path):
    code = f"import sys; sys.path.insert(0, {str(SRC)!r}); import calibrate; print(round(calibrate.calibrate(500.0), 2))"
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=tmp_path, timeout=30)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "507.0"


def test_missing_settings_file_gives_empty_settings():
    assert load_module().load_settings("does-not-exist.yaml") == {}


def test_tolerance_is_a_float_with_a_default_and_a_clear_error(monkeypatch):
    mod = load_module()
    monkeypatch.delenv("PRESSURE_TOLERANCE", raising=False)
    assert mod.tolerance_from_env() == pytest.approx(5.0)
    monkeypatch.setenv("PRESSURE_TOLERANCE", "2.5")
    assert mod.tolerance_from_env() == 2.5 and isinstance(mod.tolerance_from_env(), float)
    monkeypatch.setenv("PRESSURE_TOLERANCE", "two")
    with pytest.raises(ValueError, match="PRESSURE_TOLERANCE"):
        mod.tolerance_from_env()


def test_calibration_boundaries():
    mod = load_module()
    assert mod.calibrate(0.0) == pytest.approx(-3.0) and mod.calibrate(1000.0) == pytest.approx(1017.0)
    with pytest.raises(ValueError):
        mod.calibrate(1001.0)
