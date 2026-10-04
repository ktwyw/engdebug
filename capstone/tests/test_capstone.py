"""Capstone acceptance tests. They run against capstone/release by default; set ENGDEBUG_CAPSTONE_SRC to
point at your fixed copy. All must pass, including the performance test, before the release ships."""

import importlib
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(os.environ.get("ENGDEBUG_CAPSTONE_SRC", ROOT / "capstone" / "release"))
DATA = ROOT / "datasets"
sys.path.insert(0, str(SRC))
for name in list(sys.modules):
    if name.startswith("engdebug_release"):
        del sys.modules[name]
rel = importlib.import_module("engdebug_release")


def test_release_version():
    assert rel.__version__.startswith("0.2.0")


def test_clean_day_runs():
    result = rel.pipeline.run(DATA / "clean" / "sensor_day1.csv")
    assert len(result["summary"]) == 6


def test_corrupted_file_is_handled_not_rejected():
    """Data handling: the March file has a byte-order mark; the release refuses it as 'missing columns'."""
    result = rel.pipeline.run(DATA / "corrupted" / "sensor_day1_corrupted.csv")
    assert len(result["summary"]) == 6 and len(result["skipped"]) == 2


def test_negative_drift_is_alerted():
    """Logic: a sensor drifting downwards must alert like one drifting upwards."""
    t0 = datetime(2026, 3, 2)
    recs = [{"timestamp": t0 + timedelta(minutes=i), "sensor_id": "T102", "reading": 60.0, "unit": "degC"} for i in range(10)]
    alerts = rel.alerting.drift_alerts({"T102": recs}, {"T102": 65.0}, max_drift=2.0)
    assert len(alerts) == 1 and alerts[0]["kind"] == "drift" and alerts[0]["value"] == pytest.approx(-5.0)


def test_day2_reports_both_excursion_and_drift():
    result = rel.pipeline.run(DATA / "clean" / "sensor_day2.csv", {"references": {"T101": 72.0, "T102": 70.0}, "max_drift": 1.5})
    kinds = {(a["sensor_id"], a["kind"]) for a in result["alerts"]}
    assert ("P101", "high") in kinds and ("T101", "drift") in kinds and ("T102", "drift") in kinds


def test_month_runs_in_under_ten_seconds():
    """Performance: 0.1.0 processed a month in about two seconds; the release candidate takes minutes."""
    t0 = time.perf_counter()
    rel.pipeline.run(DATA / "clean" / "large_day.csv")
    assert time.perf_counter() - t0 < 10.0
