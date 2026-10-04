# Lab 05 · Logic bugs: the code runs, the numbers are wrong

**Context.** Nothing in `analysis.py` crashes. Every function returns a number, the dashboard shows it, and
for two months nobody has questioned it. A new engineer plotted the moving average against the raw data
and noticed the first few points were always too low. Then she kept looking.

**Time.** 75 minutes. **Prerequisites.** Labs 01-02.

## What you will learn

- the bug classes that produce no traceback: off-by-one, the wrong denominator at a boundary, unit mix-ups,
  floating-point equality, `>=` where `>` was meant, a misplaced power
- that logic bugs are found by *tests with known answers*, not by reading the code once more
- how to pick the known answers: constant series (the average of 10, 10, 10 is 10), symmetric inputs,
  tiny cases you can do by hand

## Reproduce

```bash
python -m pytest labs/lab05_logic_bugs -q
python -c "
import sys; sys.path.insert(0, 'labs/lab05_logic_bugs/buggy'); import analysis
print(analysis.moving_average([10, 10, 10, 10], 3))      # expect four tens
print(analysis.fractions_sum_to_one([0.1, 0.2, 0.7]))    # expect True
print(analysis.pressure_ok(13, 'bar'))                   # 13 bar = 1300 kPa: expect False
"
```

## Diagnose

For each function, construct one input whose correct output you know without running anything, run it,
and compare. Write the input, the expected output and the actual output in your notes before looking for
the cause. Six functions, six distinct bug classes:

| function | symptom | bug class |
|---|---|---|
| `moving_average` | first values too small | wrong denominator at the boundary |
| `drift` | slightly off, more so for short series | off-by-one (`range(1, n)`) |
| `pressure_ok` | 13 bar passes a 1200 kPa limit | unit mix-up: the unit argument is ignored |
| `fractions_sum_to_one` | 0.1 + 0.2 + 0.7 "is not 1" | floating-point `==` |
| `count_above` | counts the threshold itself | `>=` for `>` |
| `rms` | wrong for any series with more than one value | `sum(x) ** 2` for `sum(x ** 2)` |

## Fix

Fix each with the smallest change. For `fractions_sum_to_one` use `math.isclose` with a tolerance you can
justify (1e-9 relative is the usual choice; `abs_tol` matters when the expected value is zero). For
`pressure_ok`, convert to kPa first and raise `ValueError` for a unit you cannot convert - never guess.

## Prevent recurrence

Known-answer tests for every formula, with at least one constant input and one boundary. Units in
variable names (`limit_kpa`) and conversion at the boundary. Never `==` on floats (ruff has no rule for
this; your eyes do). The reference `calculations.py` has the corrected versions and
`tests/unit/test_calculations.py` the tests, including a property-based check that the moving average
matches a naive implementation for thousands of random inputs.

## Hint ladder

Use one hint at a time, only after an honest attempt.

1. For each function, pick an input whose answer you know: constants, two values, a symmetric pair.
2. `moving_average([10, 10, 10], 3)`: what does the code divide by at i = 0? `drift`: what does `range(1, n)` skip?
3. `0.1 + 0.2 == 0.3` is False; `math.isclose`. `13 bar` is `1300 kPa`.

## Deliverable

The fixed `analysis.py` (tests green) and your table of six known-answer inputs. Add one regression test
of your own for the bug you found hardest to see.
