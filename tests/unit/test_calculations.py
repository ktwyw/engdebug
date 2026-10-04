import math

import pytest
from hypothesis import given
from hypothesis import strategies as st

from engdebug import calculations as calc
from engdebug.exceptions import CalculationError


class TestEfficiency:
    def test_fraction(self):
        assert calc.efficiency(80.0, 100.0) == pytest.approx(0.8)

    @pytest.mark.parametrize("out, inp", [(1.0, 0.0), (1.0, -5.0)])
    def test_non_positive_input_raises(self, out, inp):
        with pytest.raises(CalculationError, match="input power must be positive"):
            calc.efficiency(out, inp)

    def test_output_above_input_raises(self):
        with pytest.raises(CalculationError, match="exceeds input"):
            calc.efficiency(120.0, 100.0)

    def test_negative_output_raises(self):
        with pytest.raises(CalculationError):
            calc.efficiency(-1.0, 100.0)

    def test_equal_gives_one(self):
        assert calc.efficiency(100.0, 100.0) == 1.0

    @given(st.floats(0.0, 1e6), st.floats(1e-6, 1e6))
    def test_property_in_unit_interval(self, out, inp):
        if out <= inp:
            assert 0.0 <= calc.efficiency(out, inp) <= 1.0


class TestMovingAverage:
    def test_boundary_uses_available_values(self):
        assert calc.moving_average([2, 4, 6, 8], 3) == pytest.approx([2, 3, 4, 6])

    def test_window_one_is_identity(self):
        assert calc.moving_average([1.0, 5.0, 2.0], 1) == [1.0, 5.0, 2.0]

    def test_window_larger_than_series(self):
        assert calc.moving_average([1.0, 3.0], 10) == pytest.approx([1.0, 2.0])

    def test_empty(self):
        assert calc.moving_average([], 3) == []

    @pytest.mark.parametrize("window", [0, -1])
    def test_bad_window(self, window):
        with pytest.raises(ValueError):
            calc.moving_average([1.0], window)

    @given(st.lists(st.floats(-1e6, 1e6), min_size=1, max_size=50), st.integers(1, 10))
    def test_matches_naive(self, values, window):
        naive = [
            sum(values[max(0, i - window + 1) : i + 1]) / len(values[max(0, i - window + 1) : i + 1])
            for i in range(len(values))
        ]
        assert calc.moving_average(values, window) == pytest.approx(naive, abs=1e-6)


class TestStatsAndScores:
    def test_mean_std(self):
        m, s = calc.mean_and_std([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
        assert m == 5.0 and s == pytest.approx(2.138, abs=1e-3)

    def test_single_value_std_zero(self):
        assert calc.mean_and_std([3.0]) == (3.0, 0.0)

    def test_empty_raises(self):
        with pytest.raises(CalculationError):
            calc.mean_and_std([])

    def test_anomaly_scores_flag_spike(self):
        vals = [10.0, 10.5] * 10 + [30.0]
        z = calc.anomaly_scores(vals, window=20)
        assert z[-1] > 4 and all(abs(v) < 2 for v in z[:-1])

    def test_anomaly_constant_series_zero(self):
        assert calc.anomaly_scores([5.0] * 10) == [0.0] * 10

    def test_drift(self):
        assert calc.drift([1.0, 2.0, 3.0], 1.5) == pytest.approx(0.5)

    def test_drift_empty(self):
        with pytest.raises(CalculationError):
            calc.drift([], 0.0)


class TestUnitsAndFloats:
    def test_bar_to_kpa(self):
        assert calc.to_kpa(1.0, "bar") == 100.0 and calc.to_kpa(250.0, "kPa") == 250.0

    def test_unknown_unit(self):
        with pytest.raises(CalculationError):
            calc.to_kpa(1.0, "psi")

    def test_float_comparison(self):
        assert calc.isclose(0.1 + 0.2, 0.3) and not math.isclose(0.1 + 0.2, 0.3, rel_tol=0, abs_tol=0)

    def test_interpolate(self):
        assert calc.interpolate(5.0, [0.0, 10.0], [0.0, 100.0]) == 50.0
        assert calc.interpolate(10.0, [0.0, 10.0], [0.0, 100.0]) == 100.0

    def test_interpolate_outside(self):
        with pytest.raises(CalculationError, match="outside"):
            calc.interpolate(11.0, [0.0, 10.0], [0.0, 100.0])
