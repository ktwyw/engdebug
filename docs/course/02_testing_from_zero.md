# Chapter 2 · Testing from zero

*For lab 02 (and every lab after it). Runnable example: `examples/ch02_first_test.py`.*

## Why test

You already test: you run the function, look at the number, nod. The problem is that the nod is not
recorded. Next week you change a line three functions away and the number is wrong again, and nobody
nods. A test is the nod written down so that a machine can repeat it, a thousand times, in a second,
after every change.

Three things a test suite gives you that running-and-looking does not:

1. **A specification.** To write `assert efficiency(80, 100) == 0.8` you must first decide that 80 out
   of 100 is 0.8 - not 1.25, not 80 %. Half of lab 02's bugs are resolved the moment you write down what
   correct means.
2. **Permission to change things.** With tests, you can refactor, optimise or rewrite and know within a
   second whether you broke anything. Without them, every change is a risk and the code calcifies.
3. **A place to put the bug's gravestone.** Every bug you fix becomes a test that fails if it returns
   (a *regression test*). Over a year the suite becomes the memory of every mistake the team has made.

## What a test is

A test is a function that calls your code with a known input and checks the output with `assert`:

```python
# tests/test_kpi.py
from kpi import efficiency

def test_efficiency_of_80_out_of_100_is_0_8():
    assert efficiency(80.0, 100.0) == 0.8
```

Three conventions make a test suite work without configuration: the file is called `test_*.py`, the
function is called `test_*`, and it uses `assert`. The tool that finds and runs them is `pytest`:

```bash
python -m pytest -q                 # run everything under tests/
python -m pytest tests/test_kpi.py  # one file
python -m pytest -k efficiency      # tests whose name contains "efficiency"
python -m pytest -x                 # stop at the first failure
python -m pytest --lf               # rerun only what failed last time
```

A passing test prints a dot. A failing one prints the assertion with the values on both sides, which
is the first clue in any debugging session:

```
    def test_efficiency_of_80_out_of_100_is_0_8():
>       assert efficiency(80.0, 100.0) == 0.8
E       assert 1.25 == 0.8
E        +  where 1.25 = efficiency(80.0, 100.0)
```

## The three tests every function needs

For any function, write at least:

- a **normal case**: a typical input with an answer you know (`efficiency(80, 100)` is 0.8);
- a **boundary**: the edge of the valid range (`efficiency(100, 100)` is exactly 1.0; a window of 1; an
  empty list; the largest allowed value; the value exactly on a limit - is 400.0 degC valid?);
- an **error case**: an input the function must refuse, and *how* it refuses (`efficiency(50, 0)` raises
  `ValueError` with a message naming the input power).

Boundaries are where bugs live. `range(len(x))` is right for every element except the last; a moving
average is right everywhere except the first `window - 1` points; a limit check is right everywhere
except *at* the limit. If you only test typical values, you test the part that was never going to be
wrong.

## Picking inputs whose answer you know

The hard part of a test is knowing the right answer without running the code (if you run the code to
find the expected value, you have tested that the code equals itself). Choose inputs where the answer
is obvious:

- constants: the mean of `[10, 10, 10]` is 10; the drift of a series equal to its reference is 0;
- tiny sizes: one element, two elements, where you can do the arithmetic by hand;
- symmetry: `rms([-2, 2])` is 2; `hours_between(a, b) == hours_between(b, a)`;
- an identity: a moving average with window 1 returns the input; converting bar to kPa and back is the
  identity;
- a value you can look up: a calibration table's own points interpolate to themselves.

Lab 05 is six functions that all run and are all wrong; known-answer inputs are the only way to see it.

## pytest, the parts you need

**Floats.** Never compare floats with `==`: `0.1 + 0.2 == 0.3` is `False` (chapter 5). Use
`pytest.approx`:

```python
import pytest
assert calc.moving_average([2, 4, 6], 3) == pytest.approx([2, 3, 4])
assert efficiency(1, 3) == pytest.approx(0.3333, abs=1e-4)
```

**Errors.** The error type and its message are part of what the function promises:

```python
with pytest.raises(ValueError, match="input power must be positive"):
    efficiency(50.0, 0.0)
```

If the function does not raise, or raises something else, or the message does not contain the text,
the test fails.

**Many inputs, one test.** `parametrize` runs the same test body for each row:

```python
@pytest.mark.parametrize("text, value", [("6.25", 6.25), (" 6,25 ", 6.25), ("-3", -3.0)])
def test_parse_reading(text, value):
    assert parse_reading(text) == value
```

Each row is reported separately, so you see *which* input failed.

**Shared setup: fixtures.** A fixture is a function that builds something tests need; pytest passes it in
by name:

```python
@pytest.fixture
def records():
    return [{"sensor_id": "T101", "reading": 70.0, "unit": "degC"}, ...]

def test_threshold_alerts(records):
    assert alerting.threshold_alerts(records) == []
```

`tests/conftest.py` holds the fixtures shared across files. Two built-in fixtures you will use constantly:
`tmp_path` (a fresh empty directory for each test, so tests that write files cannot interfere) and
`caplog` (captures log output, chapter 8).

**Property-based tests.** Instead of one input, state a property that holds for *all* inputs and let
`hypothesis` generate hundreds:

```python
from hypothesis import given, strategies as st

@given(st.floats(0, 1e6), st.floats(1e-6, 1e6))
def test_efficiency_is_a_fraction(out, inp):
    if out <= inp:
        assert 0.0 <= efficiency(out, inp) <= 1.0
```

When it finds a counterexample it shrinks it to the simplest one and shows you. It is the tool for
"does my fast version equal my slow version?" (lab 10) and "does this ever return a negative number?".

## Kinds of test

The names describe *what question the test answers*:

| kind | question | in this repository |
|---|---|---|
| unit | does this function do what its docstring says? | `tests/unit/` |
| integration | do these two parts fit together on real data? | `tests/integration/` |
| end-to-end | does the program work as the user runs it? | `tests/e2e/` runs the CLI in a subprocess |
| regression | does last month's bug stay fixed? | `tests/regression/`, one per lab |
| performance | is it still fast enough? | `tests/performance/` |
| smoke | does it run at all? | the first test of any suite |

Most of your tests will be unit tests, because they are small and fast and point straight at the broken
function. But a suite of only unit tests can be green while the program does not run (lab 07): the
pieces work and do not fit. One integration test per boundary catches that.

## What a good test looks like

- **One behaviour per test**, named for it: `test_bad_row_reports_row_number`, not `test_loader_2`. When
  it fails, the name is the bug report.
- **Arrange, act, assert**: build the input, call the function, check the result - in that order, in a
  few lines. A test you cannot read in ten seconds is a test nobody will maintain.
- **No logic in tests.** If you need a loop, use `parametrize`; if you need a computation to find the
  expected value, you are testing the code against itself.
- **Fails for one reason.** Two asserts about two different behaviours should be two tests.
- **Independent.** A test must not depend on another having run first, on files left behind, on the
  time of day. `tmp_path`, fixed seeds, fixtures.

## Tests first?

You do not have to write the test before the code. But for a bug, write the test first, always: a test
that fails for the exact reason the bug report describes, then the fix, then watch it pass. That order
proves the test tests the right thing - a test written after the fix may pass for the wrong reason.

## Habits this chapter starts

- **A function with no test is a draft.** Three tests - normal, boundary, error - before it goes on a
  dashboard, into a report, or into someone else's code.
- **Small, pure functions are testable; big ones are not.** A function that reads a file, computes and
  prints cannot be unit-tested; three functions (read, compute, print) can. Design for the test.
- **Name the behaviour.** `test_moving_average_start_uses_available_values` is a sentence; when it fails
  you know what broke without opening the file.
- **Run the suite before every commit.** `python -m pytest -q` takes seconds. It is the cheapest insurance
  you will ever buy.

Next: [Chapter 3 · Exceptions, assertions and error messages](03_exceptions.md).
