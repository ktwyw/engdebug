# Verification, validation and benchmarking

A one-page guide to the practice chapter 13 teaches and `tests/benchmarks/` demonstrates. Keep it next
to every engineering calculation you write.

## The two questions

- **Verification** - are we solving the equations *right*? Evidence from inside mathematics: analytical
  limits, identities, scaling laws, independent methods, convergence. The programmer can do it alone.
- **Validation** - are these the *right equations* for the real system? Evidence from outside the code:
  measurements, published reference data, worked examples from standards. Needs an engineer and data.

A verified implementation of the wrong correlation is wrong. A validated correlation with a missing ½
is wrong. Do both; record both.

## The ladder

| rung | check | cost | example in this repository |
|---|---|---|---|
| 1 | dimensional homogeneity, on paper | minutes | `rho Q H` is not a watt → `g` is missing |
| 2 | order of magnitude | minutes | water at 2 m/s in 50 mm: Re ≈ 10⁵, Δp ≈ 1 bar / 100 m |
| 3 | analytical limits and identities | one test each | f = 64/Re; LMTD(ΔT, ΔT) = ΔT; 22.414 L/mol; Darcy-Weisbach = Hagen-Poiseuille in laminar flow |
| 4 | scaling laws | one test each | doubling v quadruples a ρv² pressure drop |
| 5 | an independent method | one test each | Haaland within 2 % of Colebrook; Blasius for smooth pipes |
| 6 | published reference values and worked examples | one test each, source named | IAPWS water viscosity; the textbook 50 mm pipe case |
| 7 | convergence under refinement (numerical methods) | one test | step halved → answer settles |
| 8 | measurements from the actual system | an experiment | plant data against the model |

Reach rung 5 before a function goes on a report, rung 6 before it sizes equipment, rung 8 before it
supports a safety case.

## What a benchmark test looks like

```python
def test_ideal_gas_molar_volume_at_stp(self):
    # 1 mol at 273.15 K and 101325 Pa: 22.414 L (CODATA 2018 R)
    assert eng.ideal_gas_volume_m3(1.0, 273.15, 101325.0) == pytest.approx(0.022414, rel=1e-4)
```

The expected value, its source, a tolerance that matches the source's precision. A test whose expected
value came from running the code is a *regression* test: valuable for catching change, useless for
catching error. Keep the two in separate files (`tests/benchmarks/` and `tests/regression/`).

## The V&V record

One line per function, kept with the code, updated when either changes:

| function | verified by | validated against | trusted range |
|---|---|---|---|
| `friction_factor` | 64/Re exact; Haaland vs Colebrook 2 % | Moody chart, worked case | laminar < 2300; turbulent ≥ 4000; transition refused |
| `water_viscosity_pa_s` | - | IAPWS 2008, 1.5 % at 20-80 °C | 0-100 °C |

`solutions/lab14/NOTES.md` is a complete example. This table is what a reviewer, an auditor or a
colleague inheriting the code asks for first; without it the code is a spreadsheet with better syntax.

## Ranges

Every correlation has a range in which it was fitted. In the code it appears twice: in the docstring
("valid 0-100 °C") and in a check that raises outside it with the range in the message. Refuse
extrapolation of tables. Refuse regimes with no correlation (laminar-turbulent transition). A refused
calculation costs a phone call; an invented number costs more.

## Units

Name the unit in every parameter. SI inside; one conversion function with factors that cite their
source (NIST SP 811). Plausibility bounds at the boundary catch the classic slips: a Pa s viscosity above
0.5 is centipoise, a kelvin temperature below 100 is Celsius, an efficiency above 1 is a percentage.
Each bound is a *plant assumption* stated in the message, not physics; the day it stops holding, someone
changes it knowingly.
