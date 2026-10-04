"""Lab 05 check.  Run with:  python -m pytest labs/lab05_logic_bugs -q"""

import importlib.util
import math
import os
from pathlib import Path

import pytest

SRC = Path(os.environ.get("ENGDEBUG_LAB_SRC", Path(__file__).parent / "buggy"))
spec = importlib.util.spec_from_file_location("analysis", SRC / "analysis.py")
an = importlib.util.module_from_spec(spec)
spec.loader.exec_module(an)


def test_moving_average_start_of_series():
    assert an.moving_average([10.0, 10.0, 10.0, 10.0], 3) == pytest.approx([10.0, 10.0, 10.0, 10.0])
    assert an.moving_average([2.0, 4.0, 6.0, 8.0], 3) == pytest.approx([2.0, 3.0, 4.0, 6.0])


def test_drift_uses_every_value():
    assert an.drift([1.0, 2.0, 3.0], 2.0) == pytest.approx(0.0)
    assert an.drift([5.0], 2.0) == pytest.approx(3.0)


def test_pressure_units_are_converted():
    assert an.pressure_ok(6.0, "bar") is True          # 600 kPa
    assert an.pressure_ok(13.0, "bar") is False        # 1300 kPa
    assert an.pressure_ok(1100.0, "kPa") is True
    with pytest.raises(ValueError):
        an.pressure_ok(10.0, "psi")


def test_fractions_with_floating_point_noise():
    assert an.fractions_sum_to_one([0.1, 0.2, 0.7]) is True
    assert an.fractions_sum_to_one([0.1, 0.2, 0.6]) is False


def test_count_strictly_above():
    assert an.count_above([1.0, 2.0, 3.0], 2.0) == 1


def test_rms():
    assert an.rms([3.0, 4.0]) == pytest.approx(math.sqrt(12.5))
    assert an.rms([-2.0, 2.0]) == pytest.approx(2.0)
