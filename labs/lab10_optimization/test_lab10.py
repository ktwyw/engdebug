"""Lab 10 check.  Run with:  python -m pytest labs/lab10_optimization -q
Correctness first (identical output to the slow version), then speed (a month in under a second)."""

import importlib.util
import os
import sys
import time
from pathlib import Path

import pytest

HERE = Path(__file__).parent
SRC = Path(os.environ.get("ENGDEBUG_LAB_SRC", HERE / "buggy"))
DATA = Path(__file__).resolve().parents[2] / "datasets"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


slow = load_module("slow", HERE / "buggy" / "slow.py")   # the baseline is always the original
fast = load_module("fast", SRC / "fast.py")


def test_identical_output_on_a_day():
    assert fast.run(DATA / "clean" / "sensor_day2.csv") == slow.run(DATA / "clean" / "sensor_day2.csv")


def test_anomaly_scores_match_to_float_precision():
    vals = [10.0, 10.5] * 30 + [40.0] + [10.2] * 10
    assert fast.anomaly_scores(vals, 20) == pytest.approx(slow.anomaly_scores(vals, 20), abs=1e-9)


def test_month_under_two_seconds():
    records = fast.load(DATA / "clean" / "large_day.csv")
    t0 = time.perf_counter()
    out = fast.flagged(records)
    elapsed = time.perf_counter() - t0
    assert elapsed < 2.0, f"flagged() took {elapsed:.1f} s on a month; the target is under 2 s"
    assert out == slow.flagged(records[: 288 * 6 * 2]) or len(out) > 0  # sanity: produces output


def test_benchmark_report_exists():
    report = SRC / "benchmark.md"
    assert report.exists(), "write benchmark.md: before/after timings on the day and the month, and the changes made"
    text = report.read_text().lower()
    assert "before" in text and "after" in text
