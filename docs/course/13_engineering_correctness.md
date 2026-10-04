# Chapter 13 · Engineering correctness: units, equations, ranges - verification and validation

*For lab 14. Runnable example: `examples/ch13_units.py`. Reference: `src/engdebug/engineering.py` and
`tests/benchmarks/`.*

## The errors that cost the most

Every error in chapters 1-12 is a *programming* error: Python did something other than what the
programmer meant. This chapter is about a different family, the one specific to engineering software:
the program does exactly what the programmer meant, and **what the programmer meant is physically
wrong**. A viscosity passed in centipoise to a formula that expects pascal-seconds. A temperature in
Celsius inside the ideal gas law. A pressure drop computed without the ½. A friction-factor correlation
fitted for turbulent flow applied to laminar flow. A property table extrapolated past its last entry.

None of these produce a traceback. All of them produce a number of plausible magnitude that goes on a
report, into a sizing, into a purchase order. The Mars Climate Orbiter was lost in 1999 because one team's
software produced thrust in pound-force-seconds and the other's expected newton-seconds; the Gimli
Glider ran out of fuel at 41 000 feet because the fuel was computed in pounds and loaded in kilograms.
In a plant the consequences are smaller and far more frequent: a pump that cannot deliver the head, a
heat exchanger half the size it should be, a safety margin that was never there.

These errors are harder to find than programming errors because *nothing in the computer knows the
physics*. Python cannot tell that `temperature_c` should not be multiplied by R. Only three things can:
a person who writes units next to every number, a test whose expected value comes from outside the
code, and a process - verification and validation - that makes both routine.

## Units

**Name the unit in the name.** `viscosity_pa_s`, `temperature_k`, `pressure_pa`, `flow_m3_s`,
`efficiency` (a fraction; if it were a percentage the name would say `efficiency_pct`). A parameter
called `temperature` is an invitation to pass whatever is to hand. The name is the cheapest unit system
there is: it costs nothing at runtime and every reader checks it automatically.

**SI inside, convert at the boundary.** Internally every quantity is in one unit system (SI: m, kg, s,
K, Pa, W). Data sheets give viscosity in cP, pressure in bar, diameter in mm: convert them *once*, in the
function that reads them, through a single conversion function whose factors are named and sourced
(`_TO_SI["pressure"]["psi"] = 6894.757293168`, NIST SP 811). A conversion factor typed into a formula
(`* 100`, `/ 1000`) is a unit bug waiting to happen and impossible to search for.

**Catch the classic slips at the boundary.** Some wrong units have a signature: a "pascal-second"
viscosity above 0.5 is almost always centipoise; a "kelvin" temperature below 100 is almost always
Celsius; an "efficiency" above 1 is a percentage; a "metre" diameter above 5 is millimetres. A range
check with a message that names the suspected slip (`"was it given in cP?"`) turns a silent factor of
1000 into a clear error. The range is a *plant assumption*, not physics; state it in the message so that
the day the plant pumps glycerol, someone changes the number knowingly.

**Dimensional homogeneity is a test.** Every term of an equation must have the same dimensions. A
formula `f (L/D) ρ v²/2` has dimensions of pressure on both sides; `n R T / p` is a volume only if T is
an absolute temperature. Writing the units of each factor next to it, on paper, before coding, catches
most equation errors; it is how `pump_power = ρ Q H / η` reveals that it is missing a `g` (kg/m³ · m³/s ·
m is not a watt).

**Scaling laws are tests.** If the equation is dimensionally right, doubling the velocity must quadruple
a `ρ v²` pressure drop and double a Hagen-Poiseuille one. A test that checks the *exponent* catches a
`v` typed for `v²` without needing a reference value at all.

## Equations

**Every equation has a limit it must reproduce.** The log-mean temperature difference equals ΔT when
both ends have the same ΔT (and the formula is 0/0 there: the code must handle it). The Darcy-Weisbach
pressure drop with the laminar friction factor 64/Re is *identically* Hagen-Poiseuille's 32 μ L v / D².
One mole of ideal gas at 273.15 K and 101 325 Pa occupies 22.414 L. A pump lifting 1 m³/s by 10 m at
100 % efficiency draws exactly ρ g Q H = 98 066.5 W. These are **analytical benchmarks**: known answers
that need no experiment and no other software, and that a formula with a wrong factor cannot reproduce.
Every engineering function gets at least one.

**Two methods for one quantity.** The Haaland explicit formula and the Colebrook implicit equation give
the turbulent friction factor to within 2 % of each other; a test that computes both and compares them
catches an error in either - an **independent-method check**. The same idea: a numerical integral against
an analytical one, a vectorised NumPy routine against a plain loop, your implementation against a
colleague's.

**Order of magnitude first.** Before any test, estimate: water at 2 m/s in a 50 mm pipe gives Re ≈
10⁵; the pressure drop over 100 m is about a bar. A function returning 0.0087 bar or 87 bar is wrong
before you know *how*. Each factor has a signature: 2 is a missing half, 9.8 is g, 100 is a percentage
or centimetres, 273 is Celsius-for-kelvin, 1000 is a milli- or kilo- prefix. The engineer who can
estimate finds unit bugs in seconds; the one who cannot trusts the printout.

## Ranges of validity

A correlation is a curve fitted to data over some range of conditions. Outside that range it is not
wrong - it is *meaningless*, and the code that evaluates it has no way to know. Blasius'
f = 0.3164 Re^-0.25 was fitted for smooth pipes and 4 000 < Re < 10⁵; the Vogel viscosity correlation
for liquid water holds from 0 to 100 °C; a property table has a first and a last entry. Three rules:

- **every correlation carries its range in the code**, as a check that raises outside it and a
  docstring that states it;
- **interpolation is allowed, extrapolation is refused** unless someone writes down why it is
  acceptable this time;
- **regimes with no correlation are refused, not bridged**: laminar-turbulent transition
  (2 300 < Re < 4 000) has no reliable friction factor; a function that returns one is inventing a number.

A refused calculation is an inconvenience; an invented number is a liability.

## Verification and validation

Two questions, in this order, with different evidence:

| | question | evidence | who can answer it |
|---|---|---|---|
| **Verification** | are we solving the equations *right*? | analytical limits, identities, scaling laws, independent methods, convergence under refinement | the programmer, alone |
| **Validation** | are these the *right equations* for the real system? | measurements, published reference data, a worked example from a standard | the engineer, with data from outside |

Verification is about the code; validation is about the model. A perfectly verified implementation of
the wrong correlation is wrong; a validated correlation implemented with a missing ½ is wrong. Both
are needed and neither replaces the other.

**Benchmarking** is the practice that serves both: a test whose expected value has a *source outside
the code*, named in the test - "22.414 L, CODATA R", "1.0016 mPa s at 20 °C, IAPWS 2008", "f ≈ 0.022 from
the Moody chart at Re = 10⁵, ε/D = 10⁻³". `tests/benchmarks/test_reference_values.py` is a file of nothing
else. A test whose expected value was obtained by running the code is not a benchmark; it is a regression
test, useful for a different purpose (it catches *change*, not *error*).

**The V&V ladder**, from cheapest to most expensive:

1. dimensional homogeneity, on paper;
2. order-of-magnitude estimate;
3. analytical limits and identities;
4. scaling laws;
5. an independent method (second correlation, second implementation, hand calculation);
6. published reference values and worked examples;
7. convergence (for numerical methods: refine the step and watch the answer settle);
8. comparison with measurements from the actual system.

A function that goes on a report has climbed at least to rung 5; one that sizes equipment, to rung 6;
one whose output is a safety case, to 8. The rung reached is recorded: the **V&V record** (lab 14's
deliverable) is one line per function - verified by, validated against, trusted range - and it is the
document a reviewer or auditor asks for first.

## Writing it into the code

```python
def ideal_gas_volume_m3(n_mol: float, temperature_k: float, pressure_pa: float) -> float:
    """V = n R T / p. Temperature in kelvin; pressure absolute.
    Verified: 22.414 L for 1 mol at 273.15 K, 101325 Pa (CODATA R)."""
    if temperature_k <= 0:
        raise CalculationError(f"temperature must be in kelvin and positive, got {temperature_k}")
```

The unit in the name, the equation in the docstring with its benchmark, the range check with a
message. Three lines of discipline per function; the reference `engineering.py` applies them to pipe
flow, gases, heat exchangers and pumps, and `tests/benchmarks/` is its V&V record in executable form.

## Habits this chapter starts

- **Units in every name; SI inside; one conversion function with sourced factors.**
- **Write the units next to every number when you compute a known answer by hand** - and compute one
  before trusting any function.
- **Every equation gets an analytical benchmark; every correlation gets its range in the code.**
- **Refuse, do not invent**: no extrapolation, no bridging of regimes without a written assumption.
- **A benchmark names its source.** A test without a source outside the code is a regression test.
- **Keep the V&V record** with the code, one line per function, and update it when either changes.

This chapter closes the course's technical content; the capstone (chapter 12) applies all of it.
