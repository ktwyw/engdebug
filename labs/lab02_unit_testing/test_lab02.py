"""Lab 02 check. Before reading these tests, write your own in test_my_kpi.py (see the README).
Run with:  python -m pytest labs/lab02_unit_testing -q
"""

import importlib.util
import os
from pathlib import Path

import pytest

SRC = Path(os.environ.get("ENGDEBUG_LAB_SRC", Path(__file__).parent / "buggy"))
spec = importlib.util.spec_from_file_location("kpi", SRC / "kpi.py")
kpi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kpi)


class TestEfficiency:
    def test_direction(self):
        assert kpi.efficiency(80.0, 100.0) == pytest.approx(0.8)

    def test_equal_powers(self):
        assert kpi.efficiency(100.0, 100.0) == pytest.approx(1.0)

    @pytest.mark.parametrize("inp", [0.0, -1.0])
    def test_non_positive_input_raises(self, inp):
        with pytest.raises(ValueError):
            kpi.efficiency(50.0, inp)

    def test_output_above_input_raises(self):
        with pytest.raises(ValueError):
            kpi.efficiency(120.0, 100.0)


class TestCapacityFactor:
    def test_full_load(self):
        assert kpi.capacity_factor(energy_kwh=2400.0, rated_kw=100.0, hours=24.0) == pytest.approx(1.0)

    def test_half_load(self):
        assert kpi.capacity_factor(1200.0, 100.0, 24.0) == pytest.approx(0.5)

    def test_zero_hours_raises(self):
        with pytest.raises(ValueError):
            kpi.capacity_factor(1.0, 100.0, 0.0)


class TestSpecificEnergy:
    def test_value(self):
        assert kpi.specific_energy(50.0, 200.0) == pytest.approx(0.25)

    def test_zero_volume_raises(self):
        with pytest.raises(ValueError):
            kpi.specific_energy(50.0, 0.0)
