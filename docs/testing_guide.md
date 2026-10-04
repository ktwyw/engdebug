# Testing guide

## Classes of test, and where they live here

| class | question it answers | example in this repository |
|---|---|---|
| unit | does this function do what its docstring says? | `tests/unit/test_calculations.py` |
| integration | do these two stages fit together on real data? | `tests/integration/test_pipeline.py` |
| end-to-end / system | does the program work as the user runs it? | `tests/e2e/test_cli.py` (runs `python -m engdebug.cli`) |
| regression | does the bug we fixed last month stay fixed? | `tests/regression/test_regressions.py` (one per lab) |
| smoke / sanity | does it run at all after this change? | `test_clean_day_runs` in the capstone |
| performance | is it still fast enough on the largest realistic input? | `tests/performance/test_performance.py` |
| acceptance | may this release ship? | `capstone/tests/` |

## Approaches

- **Example-based**: a known input, a known output. Most tests. Pick inputs whose answer you know
  without running the code: constants, symmetric cases, tiny sizes.
- **Boundary-value**: the edges - empty input, one element, exactly the limit (is 400.0 degC valid?),
  one past it, zero, negative, the largest window.
- **Parametrised**: `@pytest.mark.parametrize` runs one test over many inputs; use it for tables of cases.
- **Property-based** (`hypothesis`): state a property that must hold for *all* inputs (efficiency is in
  [0, 1]; the fast moving average equals the naive one) and let the tool generate thousands.
- **Black-box**: from the specification, without reading the code. **White-box**: covering each branch
  you can see. Write black-box first; add white-box for branches the black-box tests missed.
- **Error-case**: `pytest.raises(ValueError, match="...")` - the error *type and message* are part of
  the behaviour.

## pytest in five lines

```python
import pytest
from engdebug import calculations as calc

def test_efficiency():                       # any function named test_* in a file named test_*.py
    assert calc.efficiency(80, 100) == pytest.approx(0.8)      # approx for floats, never ==
```

`python -m pytest -q` runs everything; `-k efficiency` selects by name; `-x` stops at the first
failure; `--lf` reruns the last failures; `-m "not slow"` skips the marked ones.

Fixtures (`tests/conftest.py`) build the shared inputs: `records`, `csv_file(rows)`, `data_dir`.
`tmp_path` gives each test a fresh directory; `caplog` captures logs; `capsys` captures stdout.

## Assertions and exceptions

- `assert` is for *invariants during development*: things that cannot be false if the code is right.
  `python -O` removes them, so never use `assert` to validate user input or data from a file.
- `raise ValueError("input power must be positive, got -5")` is for *conditions the caller can cause*:
  specific type, a message with the value, never a bare `except`.
- Custom exceptions (`exceptions.py`): a base class for the package, one subclass per kind, context in
  the message (`file, row 19: missing reading 'N/A'`), `raise ... from exc` to chain.

## What a good test looks like

One behaviour; a name that states it (`test_bad_row_reports_row_number`); arrange-act-assert in a few
lines; no logic in the test (if you need a loop, parametrise); fails for exactly one reason.

## Coverage

`python -m pytest --cov=engdebug --cov-report=term-missing` shows the lines no test reaches. 100 % is not
the goal; an uncovered branch that handles an error is a branch that has never been exercised, and that
is the one that will fail in production.
