"""Chapter 13: three wrong answers of plausible size - a unit slip, a missing factor, a correlation out of range -
and the analytical benchmarks that catch them.
Run:  python examples/ch13_units.py"""

import math

R_GAS, G = 8.314462618, 9.80665

# 1. units: Celsius in the ideal gas law
n, p = 1.0, 101325.0
print(
    f"molar volume at 0 degC, 1 atm: with T = 0 (Celsius) -> {n * R_GAS * 0.0 / p:.4f} m3;  with T = 273.15 K -> {n * R_GAS * 273.15 / p:.4f} m3  (benchmark 0.022414)"
)

# 2. equation: a missing factor of g
rho, Q, H = 1000.0, 1.0, 10.0
print(
    f"pump power, rho Q H = {rho * Q * H:.0f} W (not a watt: kg/m3 * m3/s * m);  rho g Q H = {rho * G * Q * H:.1f} W  (benchmark 98066.5)"
)

# 3. range: a turbulent correlation applied to laminar flow
for re in (500.0, 1000.0, 2000.0, 1e4):
    blasius = 0.3164 * re**-0.25
    exact = 64.0 / re if re < 2300 else float("nan")
    print(
        f"Re = {re:>7.0f}: Blasius {blasius:.4f}   64/Re {exact:.4f}   {'<- laminar: Blasius does not apply' if re < 2300 else ''}"
    )

# 4. the signature of each factor
print(
    "\nif your answer is off by: 2 -> a missing half; 9.8 -> g; 100 -> percent or cm; 273 -> Celsius for kelvin; 1000 -> milli/kilo prefix"
)
print(
    "dimensional check: f (L/D) rho v^2 / 2 ->",
    "[-][-][kg/m3][m2/s2] = kg/(m s2) = Pa",
    "| n R T / p -> [mol][J/(mol K)][K]/[Pa] = J/Pa = m3",
    math.isclose(1, 1),
)
