"""Lab 08 check.  Run with:  python -m pytest labs/lab08_logging -q"""

import importlib.util
import logging
import os
from pathlib import Path

SRC = Path(os.environ.get("ENGDEBUG_LAB_SRC", Path(__file__).parent / "buggy"))
DATA = Path(__file__).resolve().parents[2] / "datasets"
spec = importlib.util.spec_from_file_location("monitor", SRC / "monitor.py")
mon = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mon)


def test_day2_pressure_excursion_is_reported():
    found = mon.run(DATA / "clean" / "sensor_day2.csv")
    assert any(sid == "P101" and kind == "high" for sid, kind, _ in found)


def test_day2_temperature_drift_is_reported():
    found = mon.run(DATA / "clean" / "sensor_day2.csv")
    assert any(sid == "T101" and kind == "drift" for sid, kind, _ in found)


def test_unknown_unit_is_not_silently_unlimited(caplog):
    recs = [{"timestamp": None, "sensor_id": "X9", "reading": 1e6, "unit": "psi"}]
    with caplog.at_level(logging.WARNING):
        mon.threshold_alerts(recs)
    assert any("psi" in m for m in caplog.messages), "an unknown unit must be logged, not ignored"


def test_sensor_without_reference_is_logged_not_swallowed(caplog):
    recs = [{"timestamp": None, "sensor_id": "S102", "reading": 2950.0, "unit": "rpm"}]
    with caplog.at_level(logging.WARNING):
        mon.drift_alerts(recs)
    assert any("S102" in m for m in caplog.messages)


def test_module_uses_logging_not_print(capsys):
    mon.run(DATA / "clean" / "sensor_day2.csv")
    assert capsys.readouterr().out == ""


def test_run_logs_a_summary(caplog):
    with caplog.at_level(logging.INFO):
        mon.run(DATA / "clean" / "sensor_day2.csv")
    assert any("alert" in m.lower() for m in caplog.messages)


def test_no_broad_except_in_source():
    src = (SRC / "monitor.py").read_text()
    assert "except Exception:\n            pass" not in src and "except:\n" not in src
