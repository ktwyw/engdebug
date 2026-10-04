"""Lab 14 check: units, equations, ranges, verification and validation.
Run with:  python -m pytest labs/lab14_engineering_correctness -q
Every expected value has a source outside this code: an exact limit, an identity, an independent method,
or published reference data."""

import importlib.util
import math
import os
from pathlib import Path

import pytest

SRC = Path(os.environ.get("ENGDEBUG_LAB_SRC", Path(__file__).parent / "buggy"))
spec = importlib.util.spec_from_file_location("pipeflow", SRC / "pipeflow.py")
pf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pf)


# --- units: the function's contract names them, and a value in the wrong unit is refused or converted
def test_reynolds_takes_si_viscosity_and_refuses_centipoise():
    # water, 2 m/s, 50 mm, mu = 1.0e-3 Pa s -> Re ~ 1e5
    assert pf.reynolds(2.0, 0.05, 998.0, 1.0e-3) == pytest.approx(9.98e4, rel=1e-3)
    with pytest.raises(ValueError):
        pf.reynolds(2.0, 0.05, 998.0, 1.0)  # 1.0 is a cP value typed where Pa s was expected


def test_ideal_gas_uses_kelvin():
    assert pf.ideal_gas_volume(1.0, 273.15, 101325.0) == pytest.approx(0.022414, rel=2e-4)  # 22.414 L at STP
    with pytest.raises(ValueError):
        pf.ideal_gas_volume(1.0, 20.0, 101325.0)  # 20 K is not a plausible process temperature: a Celsius slip


def test_pump_power_has_g_and_takes_a_fraction():
    assert pf.pump_power(1.0, 10.0, 1000.0, 1.0) == pytest.approx(98066.5)  # rho g Q H
    with pytest.raises(ValueError):
        pf.pump_power(1.0, 10.0, 1000.0, 85.0)  # a percentage where a fraction is expected


# --- equations: analytical limits and identities
def test_laminar_friction_factor_is_exact():
    assert pf.friction_factor(1000.0) == pytest.approx(0.064)  # 64/Re, exact


def test_darcy_weisbach_reproduces_hagen_poiseuille_in_laminar_flow():
    mu, L, v, D, rho = 1.0e-3, 10.0, 0.05, 0.02, 998.0
    re = pf.reynolds(v, D, rho, mu)
    dp = pf.pressure_drop(pf.friction_factor(re), L, D, rho, v)
    assert dp == pytest.approx(32 * mu * L * v / D**2, rel=1e-9)


def test_lmtd_limit_and_ordering():
    assert pf.lmtd(20.0, 20.0) == pytest.approx(20.0)
    assert 10.0 < pf.lmtd(30.0, 10.0) < 30.0
    assert pf.lmtd(30.0, 10.0) == pytest.approx(20.0 / math.log(3.0))


# --- ranges of validity
def test_blasius_is_not_used_outside_its_range():
    with pytest.raises(ValueError):
        pf.friction_factor(3000.0)  # transition regime: no correlation applies
    assert pf.friction_factor(1e6, 0.0) == pytest.approx(0.0116, rel=0.05)  # beyond Blasius (1e5): Haaland/Colebrook


def test_table_does_not_extrapolate():
    with pytest.raises(ValueError):
        pf.interpolate(11.0, [0.0, 10.0], [0.0, 1.0])
    assert pf.interpolate(5.0, [0.0, 10.0], [0.0, 1.0]) == 0.5


# --- validation against reference data
@pytest.mark.parametrize("t_c, mu_mpa_s", [(20.0, 1.0016), (60.0, 0.4660)])
def test_water_viscosity_matches_reference_within_two_percent(t_c, mu_mpa_s):
    assert pf.water_viscosity(t_c) * 1e3 == pytest.approx(mu_mpa_s, rel=0.02)  # IAPWS / CRC Handbook


def test_water_viscosity_refuses_outside_validated_range():
    with pytest.raises(ValueError):
        pf.water_viscosity(150.0)
