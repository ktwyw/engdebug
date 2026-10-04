"""Lab 07 check.  Run with:  python -m pytest labs/lab07_integration -q"""

import importlib.util
import os
import sys
from pathlib import Path

import pytest

SRC = Path(os.environ.get("ENGDEBUG_LAB_SRC", Path(__file__).parent / "buggy"))
DATA = Path(__file__).resolve().parents[2] / "datasets"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SRC / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


ingest, analyse, run = load("ingest"), load("analyse"), load("run")


def test_ingest_contract_is_a_list_of_records():
    recs = ingest.load(DATA / "clean" / "sensor_day1.csv")
    assert isinstance(recs, list) and isinstance(recs[0], dict)
    assert set(recs[0]) == {"timestamp", "sensor_id", "reading", "unit"} and isinstance(recs[0]["reading"], float)


def test_analysis_consumes_the_contract():
    recs = ingest.load(DATA / "clean" / "sensor_day1.csv")
    means = analyse.sensor_means(recs)
    assert set(means) == {"T101", "P101", "W101", "T102", "P102", "S102"} and 60 < means["T101"] < 80


def test_config_key_matches_between_stages():
    recs = ingest.load(DATA / "clean" / "sensor_day2.csv")
    found = analyse.alerts(recs, run.CONFIG)
    assert any(sid == "P101" for sid, _ in found)


def test_end_to_end():
    means, found = run.main(DATA / "clean" / "sensor_day2.csv")
    assert len(means) == 6 and len(found) >= 1


def test_integration_test_exists_for_the_boundary():
    """A contract test lives next to the boundary it protects: ingest.load must return what analyse expects."""
    recs = ingest.load(DATA / "clean" / "sensor_day1.csv")
    analyse.sensor_means(recs[:3])
    with pytest.raises((TypeError, KeyError)):
        analyse.sensor_means({"sensor_id": ["T101"], "reading": [1.0]})
