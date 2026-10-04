# Lab 14 solution notes - the V&V record

| function | bug (class) | verified by | validated by | trusted range |
|---|---|---|---|---|
| `reynolds` | viscosity expected in cP (units) | Re ~ 1e5 for water at 2 m/s in 50 mm | - | mu in (0, 0.5] Pa s (the plant's fluids); a larger value is refused as a probable cP slip |
| `friction_factor` | Blasius for all Re (range) | 64/Re exact at Re = 1000; Haaland within 2 % of Colebrook at 1e4-1e6 | Moody chart reading for the worked case | laminar < 2300; turbulent >= 4000; transition refused |
| `pressure_drop` | missing /2 (equation) | equals Hagen-Poiseuille with f = 64/Re; scales with v^2 | 0.87 bar per 100 m for the worked case | - |
| `ideal_gas_volume` | Celsius (units) | 22.414 L/mol at STP | - | T >= 100 K (lower values are almost certainly Celsius) |
| `lmtd` | log the wrong way (equation); equal ends 0/0 | limit dT1 = dT2; between the ends; 20/ln 3 | - | both differences positive |
| `pump_power` | no g; percent (equation + units) | rho g Q H for the unit case | - | efficiency in (0, 1] |
| `water_viscosity` | a constant (validation) | - | IAPWS 1.0016, 0.6527, 0.4660, 0.3545 mPa s at 20-80 degC, within 1.5 % | 0-100 degC |
| `interpolate` | silent extrapolation (range) | midpoint of a two-point table | - | inside the table |

The order of magnitude of each error is the clue: a factor of 2 is a missing half, 9.8 is g, 100 is
percent or cm, 273 is kelvin, 1000 is a milli-prefix. Writing units next to every number while
computing a known answer by hand finds all of them before any code is run.
