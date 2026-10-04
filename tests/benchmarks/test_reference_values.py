"""Verification and validation of engdebug.engineering against sources outside the code.

Verification (are the equations solved right?): analytical limits, identities between two formulas,
an independent numerical method. Validation (are the equations right for reality?): published reference
values. Every expected number names its source.
"""

import pytest

from engdebug import engineering as eng
from engdebug.exceptions import CalculationError


class TestUnits:
    @pytest.mark.parametrize(
        "value, a, b, expected, source",
        [
            (1.0, "bar", "Pa", 1e5, "definition"),
            (1.0, "psi", "Pa", 6894.757, "NIST SP 811"),
            (1.0, "atm", "kPa", 101.325, "definition"),
            (1.0, "in", "mm", 25.4, "definition (exact since 1959)"),
            (1.0, "cP", "Pa*s", 1e-3, "definition"),
            (1.0, "m3/h", "L/s", 1 / 3.6, "arithmetic"),
            (1.0, "hp", "W", 745.6999, "mechanical horsepower, NIST SP 811"),
        ],
    )
    def test_conversion_against_source(self, value, a, b, expected, source):
        assert eng.convert(value, a, b) == pytest.approx(expected, rel=1e-6), source

    def test_round_trip_is_identity(self):
        assert eng.convert(eng.convert(3.7, "bar", "psi"), "psi", "bar") == pytest.approx(3.7)

    def test_mixing_quantities_raises(self):
        with pytest.raises(CalculationError, match="cannot convert"):
            eng.convert(1.0, "bar", "mm")

    def test_absolute_zero_is_a_boundary(self):
        assert eng.celsius_to_kelvin(0.0) == 273.15
        with pytest.raises(CalculationError):
            eng.celsius_to_kelvin(-300.0)


class TestVerificationAnalyticalLimits:
    def test_laminar_friction_factor_is_64_over_re(self):
        assert eng.friction_factor(1000.0) == pytest.approx(0.064)

    def test_darcy_weisbach_with_laminar_f_reproduces_hagen_poiseuille(self):
        mu, L, v, D, rho = 1.0e-3, 10.0, 0.05, 0.02, 998.0
        re = eng.reynolds(v, D, rho, mu)
        assert re < 2300
        dp_darcy = eng.pressure_drop_pa(eng.friction_factor(re), L, D, rho, v)
        assert dp_darcy == pytest.approx(eng.hagen_poiseuille_pa(mu, L, v, D), rel=1e-12)

    def test_lmtd_limit_of_equal_differences(self):
        assert eng.lmtd(20.0, 20.0) == 20.0
        assert eng.lmtd(20.0, 20.0 + 1e-6) == pytest.approx(20.0, abs=1e-5)

    def test_lmtd_lies_between_the_two_differences(self):
        assert 10.0 < eng.lmtd(30.0, 10.0) < 30.0

    def test_ideal_gas_molar_volume_at_stp(self):
        # 1 mol at 273.15 K and 101325 Pa: 22.414 L (CODATA R)
        assert eng.ideal_gas_volume_m3(1.0, 273.15, 101325.0) == pytest.approx(0.022414, rel=1e-4)

    def test_pump_power_unit_case(self):
        # 1 m3/s of water lifted 10 m at 100 % efficiency: rho g Q H = 98066.5 W
        assert eng.pump_power_w(1.0, 10.0, 1000.0, 1.0) == pytest.approx(98066.5)

    def test_scaling_laws(self):
        # dimensional homogeneity: doubling velocity quadruples the turbulent pressure drop at fixed f
        f, L, D, rho = 0.02, 100.0, 0.05, 998.0
        assert eng.pressure_drop_pa(f, L, D, rho, 2.0) == pytest.approx(4 * eng.pressure_drop_pa(f, L, D, rho, 1.0))
        # and doubles the laminar one (Hagen-Poiseuille is linear in v)
        assert eng.hagen_poiseuille_pa(1e-3, L, 0.02, D) == pytest.approx(2 * eng.hagen_poiseuille_pa(1e-3, L, 0.01, D))


class TestVerificationIndependentMethod:
    @pytest.mark.parametrize("re, rr", [(1e4, 0.0), (1e5, 1e-4), (1e6, 1e-3), (5e4, 1e-2)])
    def test_haaland_within_two_percent_of_colebrook(self, re, rr):
        assert eng.friction_factor(re, rr) == pytest.approx(eng.friction_factor_colebrook(re, rr), rel=0.02)

    def test_smooth_pipe_against_blasius(self):
        # Blasius f = 0.3164 Re^-0.25, valid 4000 < Re < 1e5 (smooth): a third, older correlation
        for re in (1e4, 5e4):
            assert eng.friction_factor(re, 0.0) == pytest.approx(0.3164 * re**-0.25, rel=0.03)


class TestValidationReferenceData:
    @pytest.mark.parametrize("t_c, mu_mpa_s", [(20.0, 1.0016), (40.0, 0.6527), (60.0, 0.4660), (80.0, 0.3545)])
    def test_water_viscosity_against_iapws(self, t_c, mu_mpa_s):
        # reference: IAPWS 2008 release on viscosity (values tabulated in the CRC Handbook)
        assert eng.water_viscosity_pa_s(t_c) * 1e3 == pytest.approx(mu_mpa_s, rel=0.015)

    def test_worked_example_water_in_a_50_mm_pipe(self):
        # a textbook-style case: water 20 degC, D = 50 mm, v = 2 m/s, L = 100 m, drawn steel (eps = 0.046 mm)
        rho, mu = 998.2, eng.water_viscosity_pa_s(20.0)
        D = eng.convert(50.0, "mm", "m")
        re = eng.reynolds(2.0, D, rho, mu)
        assert re == pytest.approx(9.97e4, rel=0.02)
        f = eng.friction_factor(re, 0.046e-3 / D)
        assert f == pytest.approx(0.0219, rel=0.03)  # Colebrook for Re = 1e5, eps/D = 9.2e-4 (Moody chart: about 0.022)
        dp = eng.pressure_drop_pa(f, 100.0, D, rho, 2.0)
        assert eng.convert(dp, "Pa", "bar") == pytest.approx(0.87, rel=0.05)  # about 0.87 bar per 100 m


class TestRangesOfValidity:
    def test_transition_regime_refused(self):
        with pytest.raises(CalculationError, match="transition"):
            eng.friction_factor(3000.0)

    def test_roughness_range(self):
        with pytest.raises(CalculationError, match="roughness"):
            eng.friction_factor(1e5, 0.1)

    def test_viscosity_in_cp_is_caught(self):
        with pytest.raises(CalculationError, match="cP"):
            eng.reynolds(1.0, 0.05, 1000.0, 1000.0)

    def test_celsius_into_ideal_gas_is_caught(self):
        with pytest.raises(CalculationError, match="kelvin"):
            eng.ideal_gas_volume_m3(1.0, -20.0, 101325.0)

    def test_correlation_outside_its_range(self):
        with pytest.raises(CalculationError, match="0-100"):
            eng.water_viscosity_pa_s(150.0)

    def test_extrapolation_refused(self):
        with pytest.raises(CalculationError, match="extrapolation"):
            eng.interpolate_table(11.0, [0.0, 10.0], [0.0, 1.0])
        assert eng.interpolate_table(5.0, [0.0, 10.0], [0.0, 1.0]) == 0.5

    def test_efficiency_above_one_refused(self):
        with pytest.raises(CalculationError, match="fraction"):
            eng.pump_power_w(1.0, 1.0, 1000.0, 85.0)
