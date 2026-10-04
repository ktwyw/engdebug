# Tests for the reference pipeline

```bash
python -m pytest -q                       # everything (about ten seconds)
python -m pytest -q -m "not slow"         # skip the performance tests
python -m pytest tests/unit -q            # one level
python -m pytest -k efficiency -q         # by name
python -m pytest -x --pdb                 # stop at the first failure and open the debugger
python -m pytest --cov=engdebug --cov-report=term-missing   # which lines no test reaches
```

| directory | question the tests answer | how they get their inputs |
|---|---|---|
| `unit/` | does each function do what its docstring says? | hand-made values and the `records` fixture; Hypothesis for properties |
| `integration/` | do the stages fit together on real files? | `datasets/clean` and `datasets/corrupted` |
| `e2e/` | does the program work as a user runs it? | the CLI in a subprocess; the chapter examples |
| `regression/` | does every bug fixed in a lab stay fixed? | one test per lab, named after it |
| `performance/` | is it still fast enough on a month of data? | `datasets/clean/large_day.csv`, marked `slow` |

`conftest.py` holds the shared fixtures: `data_dir` (the datasets folder), `records` (twelve clean
records for two sensors), `csv_file(rows, ...)` (writes a temporary CSV with optional BOM and CRLF).

When you fix a bug in a lab, add the equivalent regression test here, against the reference package,
named `test_labNN_<what_it_guards>`.
