# Lab 14 · Engineering correctness: units, equations, ranges - verification and validation

**Read first.** [Chapter 13 · Engineering correctness](../../docs/course/13_engineering_correctness.md) explains every concept this lab uses. **Habits practised:** units in every name, SI inside and conversion at the boundary; every equation checked against a limit it must reproduce; every correlation carries its range; benchmark before you trust (see [`docs/habits.md`](../../docs/habits.md)).

**Context.** The plant replaced a sizing spreadsheet with `pipeflow.py`. The spreadsheet had been checked
against a textbook example by the engineer who wrote it, twenty years ago. The module was checked by
the fact that it runs. Its pressure drops are twice too high, its gas volumes are a hundred times too
small, its pump powers are off by a factor of ten, and a correlation is being used for flows it was
never meant for. Every function returns a plausible-looking number. That is why these are the hardest
bugs in engineering software.

**Time.** 90 minutes. **Prerequisites.** Lab 05 (logic bugs), chapter 13.

## What you will learn

- the three engineering error classes that no traceback reports: wrong **units** (cP for Pa s, Celsius for
  kelvin, percent for a fraction, mm for m), wrong **equations** (a missing /2, a missing g, a log the
  wrong way up), and **ranges of validity** (a correlation used outside the regime it was fitted in, a
  table extrapolated, a temperature below absolute zero)
- **verification**: does the code solve the equations correctly? - checked with analytical limits
  (f = 64/Re), identities (Darcy-Weisbach with the laminar f must equal Hagen-Poiseuille), scaling laws
  (doubling v quadruples a turbulent pressure drop), and an independent method (Haaland against Colebrook)
- **validation**: are the equations right for the real fluid? - checked against published reference data
  (IAPWS water viscosity) and a worked textbook case
- **benchmarking**: a test whose expected value has a source *outside the code*, named in the test

## Reproduce

```bash
python -m pytest labs/lab14_engineering_correctness -q
python -c "
import sys; sys.path.insert(0, 'labs/lab14_engineering_correctness/buggy'); import pipeflow as pf
print('molar volume at STP (expect 0.0224 m3):', pf.ideal_gas_volume(1.0, 0.0, 101325.0))
print('laminar f at Re = 1000 (expect 0.064):', pf.friction_factor(1000.0))
print('pump power 1 m3/s x 10 m (expect 98066 W):', pf.pump_power(1.0, 10.0, 1000.0, 100))
"
```

## Observe

For each function, write down three things: the units it *says* it takes (docstring and parameter
names - what do they tell you?), one limiting case whose answer you know from physics, and the range in
which its equation is valid. Do this before running anything. Half the bugs are visible from the
docstrings alone: a Reynolds number "with viscosity as the data sheet gives it (cP)" and a gas volume
taking `temperature_c`.

## Diagnose

| function | known answer | what the code gives | class |
|---|---|---|---|
| `reynolds` | water, 2 m/s, 50 mm: Re ~ 1e5 with mu = 1e-3 Pa s | 1e5 only if you pass 1e-3 - but the docstring asks for cP, so callers pass 1.0 and get 100 | units (cP vs Pa s) |
| `friction_factor` | 64/Re = 0.064 at Re = 1000 | Blasius: 0.0563 | range: a turbulent correlation applied to laminar flow (and above 1e5) |
| `pressure_drop` | must equal Hagen-Poiseuille in laminar flow | twice too high | equation: the /2 of rho v^2/2 |
| `ideal_gas_volume` | 22.414 L per mol at 0 degC, 1 atm | 0 L | units: Celsius in a formula that needs kelvin |
| `lmtd` | 20 when both ends are 20; between the ends otherwise | negative, and 0/0 at equal ends | equation: log(dT2/dT1) flips the sign; the limit is unhandled |
| `pump_power` | rho g Q H = 98 066 W for 1 m3/s, 10 m | 10 000 / efficiency_pct | equation (no g) and units (percent, not fraction) |
| `water_viscosity` | 1.0016 mPa s at 20 degC, 0.466 at 60 | 1.0 at every temperature | validation: a constant is not a property |
| `interpolate` | refuse x outside the table | extrapolates silently | range |

## Fix

Rewrite each function with SI units named in the parameters (`viscosity_pa_s`, `temperature_k`,
`efficiency` as a fraction), the equation checked against its limit, and a `ValueError` for inputs
outside the range where the equation holds - with a message that says what the range is. For
`friction_factor`: 64/Re below 2300, Haaland above 4000, refuse the transition. For
`water_viscosity`: a Vogel-type correlation valid 0-100 degC (the reference module `engdebug.engineering`
has one); refuse outside. For `interpolate`: refuse to extrapolate.

## Prevent recurrence

The reference module `src/engdebug/engineering.py` and its benchmark suite `tests/benchmarks/` are the
template: units in every name, SI inside, conversions through one function, every correlation with its
range, and a test file where every expected value names its source - an exact limit, an identity, an
independent method, or a published table. That file is the plant's new spreadsheet check, and it runs on
every commit.

## Hint ladder

1. Compute each known answer by hand with units written out (kg, m, s). Which function's output has the
   wrong magnitude, and by what factor? Factors of 2, 9.8, 100, 273 and 1000 each point at a cause.
2. For `friction_factor`, plot or print f against Re from 500 to 1e6 with the buggy function and with
   64/Re: where do they diverge, and what regime is that?
3. The reference module `engdebug.engineering` solves the same problems; compare signatures before
   reading bodies.

## Deliverable

The fixed `pipeflow.py` (tests green) and a one-page **V&V record**: for each function, the limit or
identity used to verify it, the reference value used to validate it (with its source), and the range in
which you now trust it. This is the document a reviewer, an auditor or your future self needs; the code
without it is a spreadsheet with better syntax.
