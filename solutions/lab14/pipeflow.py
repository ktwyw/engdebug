"""Pipe-flow and utility calculations (fixed): SI units in every name, ranges enforced, equations
verified against limits in test_lab14.py. Mirrors engdebug.engineering."""

import math

R_GAS = 8.314462618
G = 9.80665


def reynolds(velocity_m_s, diameter_m, density_kg_m3, viscosity_pa_s):
    """Re = rho v D / mu, all SI. 1 cP = 1e-3 Pa s. The plant's fluids are below 0.5 Pa s (water 1e-3,
    heavy oils ~0.3); a larger value is almost certainly a cP value typed where Pa s was expected. That
    bound is a plant assumption, stated in the message, not a law of physics."""
    if viscosity_pa_s <= 0 or viscosity_pa_s > 0.5:
        raise ValueError(f"viscosity {viscosity_pa_s} Pa s is outside the plant's fluids (< 0.5 Pa s): was it given in cP? (1 cP = 1e-3 Pa s)")
    return density_kg_m3 * abs(velocity_m_s) * diameter_m / viscosity_pa_s


def friction_factor(re, relative_roughness=0.0):
    """Darcy friction factor: 64/Re laminar (exact), Haaland for Re >= 4000; the transition is refused."""
    if re <= 0:
        raise ValueError(f"Reynolds number must be positive, got {re}")
    if re < 2300:
        return 64.0 / re
    if re < 4000:
        raise ValueError(f"Re = {re:.0f} is in the transition regime (2300-4000): no correlation applies")
    return (-1.8 * math.log10((relative_roughness / 3.7) ** 1.11 + 6.9 / re)) ** -2


def pressure_drop(f, length_m, diameter_m, density_kg_m3, velocity_m_s):
    """Darcy-Weisbach: f (L/D) rho v^2 / 2 - the /2 was missing."""
    return f * (length_m / diameter_m) * density_kg_m3 * velocity_m_s**2 / 2.0


def ideal_gas_volume(n_mol, temperature_k, pressure_pa):
    """V = n R T / p with T in kelvin."""
    if temperature_k < 100.0:
        raise ValueError(f"temperature {temperature_k} K is implausible: was it given in degrees Celsius?")
    return n_mol * R_GAS * temperature_k / pressure_pa


def lmtd(dt1_k, dt2_k):
    """(dT1 - dT2) / ln(dT1/dT2); the limit dT1 = dT2 is dT."""
    if dt1_k <= 0 or dt2_k <= 0:
        raise ValueError("temperature differences must be positive at both ends")
    if math.isclose(dt1_k, dt2_k, rel_tol=1e-9):
        return dt1_k
    return (dt1_k - dt2_k) / math.log(dt1_k / dt2_k)


def pump_power(flow_m3_s, head_m, density_kg_m3, efficiency):
    """P = rho g Q H / eta, efficiency a fraction in (0, 1]."""
    if not (0 < efficiency <= 1):
        raise ValueError(f"efficiency must be a fraction in (0, 1], got {efficiency} (a percentage?)")
    return density_kg_m3 * G * flow_m3_s * head_m / efficiency


def water_viscosity(temperature_c):
    """Vogel-type correlation, valid 0-100 degC within about 1 % of IAPWS values."""
    if not (0.0 <= temperature_c <= 100.0):
        raise ValueError(f"water viscosity correlation valid for 0-100 degC, got {temperature_c}")
    return 0.02939e-3 * math.exp(507.88 / (temperature_c + 273.15 - 149.3))


def interpolate(x, xs, ys):
    """Linear interpolation inside the table only."""
    if x < xs[0] or x > xs[-1]:
        raise ValueError(f"x = {x} outside the table range [{xs[0]}, {xs[-1]}]: extrapolation refused")
    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]:
            t = (x - xs[i]) / (xs[i + 1] - xs[i])
            return ys[i] + t * (ys[i + 1] - ys[i])
    return ys[-1]
