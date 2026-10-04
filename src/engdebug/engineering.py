"""Engineering calculations with their units, ranges of validity and benchmarks made explicit.

Every function names its units in its parameters (`velocity_m_s`, `pressure_pa`), checks the range in
which its equation is valid, and is verified in `tests/benchmarks/` against analytical limits, published
reference values and an independent method. This module is the model for lab 14.

Conventions: SI inside (m, s, kg, Pa, K, W); conversions at the boundary through `convert`.
"""

from __future__ import annotations

import math

from .exceptions import CalculationError

R_GAS = 8.314462618  # J/(mol K), CODATA 2018 (exact)
G = 9.80665  # m/s^2, standard gravity (exact)

# conversion factors TO SI, grouped by quantity; a value converts between two units of the same quantity
_TO_SI = {
    "pressure": {"Pa": 1.0, "kPa": 1e3, "bar": 1e5, "psi": 6894.757293168, "atm": 101325.0},
    "length": {"m": 1.0, "mm": 1e-3, "cm": 1e-2, "in": 0.0254, "ft": 0.3048},
    "viscosity": {"Pa*s": 1.0, "mPa*s": 1e-3, "cP": 1e-3},
    "volume_flow": {"m3/s": 1.0, "m3/h": 1 / 3600, "L/s": 1e-3, "L/min": 1e-3 / 60},
    "power": {"W": 1.0, "kW": 1e3, "hp": 745.6998715823},
}


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between units of the same quantity (pressure, length, viscosity, volume flow, power).
    Temperatures are converted by `celsius_to_kelvin`; mixing quantities raises."""
    for quantity, table in _TO_SI.items():
        if from_unit in table and to_unit in table:
            return value * table[from_unit] / table[to_unit]
        if (from_unit in table) != (to_unit in table):
            raise CalculationError(f"cannot convert {quantity} unit {from_unit!r} to {to_unit!r}")
    raise CalculationError(
        f"unknown units {from_unit!r} -> {to_unit!r}; known: {sorted(u for t in _TO_SI.values() for u in t)}"
    )


def celsius_to_kelvin(temperature_c: float) -> float:
    k = temperature_c + 273.15
    if k < 0:
        raise CalculationError(f"temperature {temperature_c} degC is below absolute zero")
    return k


def reynolds(velocity_m_s: float, diameter_m: float, density_kg_m3: float, viscosity_pa_s: float) -> float:
    """Re = rho v D / mu (dimensionless). All inputs SI; viscosity in Pa s (1 cP = 1e-3 Pa s)."""
    for name, v in (("diameter_m", diameter_m), ("density_kg_m3", density_kg_m3), ("viscosity_pa_s", viscosity_pa_s)):
        if v <= 0:
            raise CalculationError(f"{name} must be positive, got {v}")
    if viscosity_pa_s > 0.5:  # water 1e-3, heavy oils ~0.3: a larger value is almost always a cP value in a Pa s slot
        raise CalculationError(
            f"viscosity {viscosity_pa_s} Pa s is outside the fluids this module is validated for (< 0.5 Pa s): was it given in cP?"
        )
    return density_kg_m3 * abs(velocity_m_s) * diameter_m / viscosity_pa_s


def friction_factor(re: float, relative_roughness: float = 0.0) -> float:
    """Darcy friction factor. Laminar (Re < 2300): 64/Re (exact). Turbulent (Re >= 4000): Haaland (1983),
    within about 2 % of Colebrook. The transition 2300 <= Re < 4000 has no reliable correlation: raises."""
    if re <= 0:
        raise CalculationError(f"Reynolds number must be positive, got {re}")
    if re < 2300:
        return 64.0 / re
    if re < 4000:
        raise CalculationError(
            f"Re = {re:.0f} is in the transition regime (2300-4000): no correlation applies; change the flow or state an assumption"
        )
    if not (0 <= relative_roughness < 0.05):
        raise CalculationError(f"relative roughness {relative_roughness} outside Haaland's range [0, 0.05)")
    return (-1.8 * math.log10((relative_roughness / 3.7) ** 1.11 + 6.9 / re)) ** -2


def friction_factor_colebrook(re: float, relative_roughness: float = 0.0, tol: float = 1e-10) -> float:
    """The implicit Colebrook equation solved by fixed-point iteration: the independent method used to
    verify `friction_factor` in the turbulent regime."""
    if re < 4000:
        raise CalculationError("Colebrook applies to turbulent flow (Re >= 4000)")
    f = 0.02
    for _ in range(200):
        f_new = (-2.0 * math.log10(relative_roughness / 3.7 + 2.51 / (re * math.sqrt(f)))) ** -2
        if abs(f_new - f) < tol:
            return f_new
        f = f_new
    raise CalculationError("Colebrook iteration did not converge")


def pressure_drop_pa(
    friction: float, length_m: float, diameter_m: float, density_kg_m3: float, velocity_m_s: float
) -> float:
    """Darcy-Weisbach: dp = f (L/D) rho v^2 / 2."""
    if length_m < 0 or diameter_m <= 0:
        raise CalculationError(f"length {length_m} m and diameter {diameter_m} m must be positive")
    return friction * (length_m / diameter_m) * density_kg_m3 * velocity_m_s**2 / 2.0


def hagen_poiseuille_pa(viscosity_pa_s: float, length_m: float, velocity_m_s: float, diameter_m: float) -> float:
    """Laminar pressure drop dp = 32 mu L v / D^2: the analytical result Darcy-Weisbach with f = 64/Re must reproduce."""
    return 32.0 * viscosity_pa_s * length_m * velocity_m_s / diameter_m**2


def ideal_gas_volume_m3(n_mol: float, temperature_k: float, pressure_pa: float) -> float:
    """V = n R T / p. Temperature in kelvin (a Celsius value here is the classic error); pressure absolute."""
    if temperature_k <= 0:
        raise CalculationError(f"temperature must be in kelvin and positive, got {temperature_k}")
    if pressure_pa <= 0:
        raise CalculationError(f"pressure must be absolute and positive, got {pressure_pa}")
    return n_mol * R_GAS * temperature_k / pressure_pa


def lmtd(delta_t1_k: float, delta_t2_k: float) -> float:
    """Log-mean temperature difference (dT1 - dT2) / ln(dT1/dT2); equals dT when the two are equal."""
    if delta_t1_k <= 0 or delta_t2_k <= 0:
        raise CalculationError(f"temperature differences must be positive at both ends, got {delta_t1_k}, {delta_t2_k}")
    if math.isclose(delta_t1_k, delta_t2_k, rel_tol=1e-9):
        return delta_t1_k
    return (delta_t1_k - delta_t2_k) / math.log(delta_t1_k / delta_t2_k)


def pump_power_w(flow_m3_s: float, head_m: float, density_kg_m3: float, efficiency: float) -> float:
    """Shaft power P = rho g Q H / eta."""
    if not (0 < efficiency <= 1):
        raise CalculationError(f"efficiency must be a fraction in (0, 1], got {efficiency}")
    if flow_m3_s < 0 or head_m < 0:
        raise CalculationError("flow and head must be non-negative")
    return density_kg_m3 * G * flow_m3_s * head_m / efficiency


def water_viscosity_pa_s(temperature_c: float) -> float:
    """Dynamic viscosity of liquid water by a Vogel-type correlation, valid 0-100 degC (within about 1 %
    of IAPWS reference values); outside that range the correlation is not validated and raises."""
    if not (0.0 <= temperature_c <= 100.0):
        raise CalculationError(f"water viscosity correlation valid for 0-100 degC, got {temperature_c}")
    t_k = temperature_c + 273.15
    return 0.02939e-3 * math.exp(507.88 / (t_k - 149.3))


def interpolate_table(x: float, xs: list[float], ys: list[float]) -> float:
    """Linear interpolation within a table; refuses to extrapolate (an extrapolated value has no basis)."""
    if len(xs) != len(ys) or len(xs) < 2 or any(b <= a for a, b in zip(xs, xs[1:])):
        raise CalculationError("table needs at least two points with strictly increasing x")
    if x < xs[0] or x > xs[-1]:
        raise CalculationError(f"x = {x} outside the table range [{xs[0]}, {xs[-1]}]: extrapolation refused")
    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]:
            t = (x - xs[i]) / (xs[i + 1] - xs[i])
            return ys[i] + t * (ys[i + 1] - ys[i])
    return ys[-1]
