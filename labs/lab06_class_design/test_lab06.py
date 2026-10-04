"""Lab 06 check.  Run with:  python -m pytest labs/lab06_class_design -q"""

import importlib.util
import os
from datetime import datetime, timedelta
from pathlib import Path

import pytest

SRC = Path(os.environ.get("ENGDEBUG_LAB_SRC", Path(__file__).parent / "buggy"))
spec = importlib.util.spec_from_file_location("equipment", SRC / "equipment.py")
eq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eq)
T0 = datetime(2026, 3, 2)


def test_readings_are_not_shared_between_sensors():
    a, b = eq.Sensor("A", "degC"), eq.Sensor("B", "degC")
    a.add(T0, 1.0)
    assert b.readings == [] and a.readings == [(T0, 1.0)]


def test_history_is_per_instance_not_per_class():
    a, b = eq.Sensor("A", "degC"), eq.Sensor("B", "degC")
    a.add(T0, 1.0)
    assert b.history == [] and a.history == ["A"]


def test_latest_and_mean_on_empty_sensor():
    s = eq.Sensor("A", "degC")
    assert s.latest() is None
    with pytest.raises(ValueError):
        s.mean()


def test_readings_must_be_in_time_order():
    s = eq.Sensor("A", "degC")
    s.add(T0 + timedelta(minutes=5), 1.0)
    with pytest.raises(ValueError):
        s.add(T0, 2.0)


def test_status_transitions_are_enforced():
    p = eq.Equipment("pump1")
    p.set_status("running")
    p.set_status("fault")
    with pytest.raises(ValueError):
        p.set_status("running")
    p.set_status("maintenance")
    assert p.status == "maintenance"
    with pytest.raises(ValueError):
        p.set_status("exploded")


def test_cannot_attach_the_same_sensor_twice():
    p = eq.Equipment("pump1")
    s = eq.Sensor("A", "degC")
    p.attach(s)
    with pytest.raises(ValueError):
        p.attach(s)


def test_equal_equipment_is_hashable_and_consistent():
    a, b = eq.Equipment("pump1"), eq.Equipment("pump1")
    assert a == b and hash(a) == hash(b)
    assert len({a, b}) == 1
    assert (a == "pump1") is False
