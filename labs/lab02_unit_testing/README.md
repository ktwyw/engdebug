# Lab 02 · Unit test rescue

**Context.** `kpi.py` computes three indicators that go on the plant's weekly dashboard. The operators say
the efficiency "looks wrong" and nobody has written a single test. You will write the tests first, watch
them fail, then fix the code.

**Time.** 75 minutes. **Prerequisites.** Lab 01; `pip install pytest`.

## What you will learn

- what a unit test is: one function, one behaviour, one assertion you can read in five seconds
- the three kinds of test every function needs: a normal case, a boundary, and an error case
- `pytest.approx` for floats, `pytest.raises` for errors, `parametrize` for several inputs at once
- that a test is a specification: writing it forces you to decide what *correct* means

## Reproduce

```bash
python -c "import sys; sys.path.insert(0, 'labs/lab02_unit_testing/buggy'); import kpi; print(kpi.efficiency(80, 100))"
```

Efficiency 1.25 for a pump that delivers 80 kW from 100 kW. Something is inverted.

## Your tests first

Create `labs/lab02_unit_testing/test_my_kpi.py` and, *before* changing `kpi.py*, write tests that
express what each function should do:

1. `efficiency(80, 100)` is 0.8; `efficiency(100, 100)` is 1.0.
2. `efficiency` must refuse a zero or negative input power (a stopped machine has no efficiency) and an
   output larger than the input (a sensor fault, not a 125 % pump). Decide which exception; `ValueError`
   is the conventional choice for "the arguments are wrong".
3. `capacity_factor(2400 kWh, 100 kW, 24 h)` is 1.0 - read the formula before you trust the code.
4. `specific_energy` must refuse a zero volume.

Run `python -m pytest labs/lab02_unit_testing -q` and count the failures. Then open `test_lab02.py` and
compare with your tests: did you think of the same boundaries?

## Diagnose and fix

Three functions, three different kinds of bug. One has the formula upside down, one has the right numbers
in the wrong order of operations, and one is "correct" but has no guard. Fix each with the smallest change
that makes the tests pass, and add the guards with messages that say what was wrong
(`f"input power must be positive, got {input_kw}"`).

## Prevent recurrence

Every function that goes on a dashboard gets three tests before it is merged: normal, boundary, error.
In the reference package, `tests/unit/test_calculations.py` shows the same functions with a
property-based test on top (Hypothesis generates thousands of inputs and checks that efficiency stays
in [0, 1]).

## Hint ladder

Use one hint at a time, only after an honest attempt.

1. Compute `efficiency(80, 100)` by hand; compare with what the code returns.
2. Python evaluates `a / b * c` as `(a / b) * c`; is that the formula on the whiteboard?
3. A guard is an `if` that raises `ValueError` with the offending value in the message.

## Deliverable

`test_my_kpi.py` (your tests), the fixed `kpi.py`, and all checks green. In your lab notes, list one
boundary case the provided tests cover that you had missed, and one you covered that they do not.
