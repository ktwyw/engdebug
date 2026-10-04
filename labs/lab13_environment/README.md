# Lab 13 · Environment, imports and configuration: "it works on my machine"

**Read first.** [Chapter 11 · Environments and configuration](../../docs/course/11_environment.md) explains every concept this lab uses. **Habits practised:** one virtual environment per project; every import declared; paths from __file__ or from arguments; configuration read once, converted once, defaulted once (see [`docs/habits.md`](../../docs/habits.md)).


**Context.** `calibrate.py` applies the pressure-sensor calibration table. On the author's laptop it is
fine. On the CI runner it fails with `ModuleNotFoundError: No module named 'yaml'`. On the operator's
machine, started from a different folder, it fails with `FileNotFoundError:
'datasets/clean/calibration.csv'`. On the scheduler it crashes with `KeyError: 'PRESSURE_TOLERANCE'`, and
when someone sets the variable, with a `TypeError` three functions later.

**Time.** 45 minutes. **Prerequisites.** Labs 01, 03, 11.

## What you will learn

- the three ways an environment differs from yours: installed packages, the working directory, and
  environment variables / configuration
- `ModuleNotFoundError` for an undeclared dependency, and the choices: declare it in `pyproject.toml`,
  make it optional with a guarded import, or drop it (here: use `json`, which is in the standard library)
- paths relative to the *current working directory* versus paths relative to the *file*
  (`Path(__file__).resolve().parent`)
- configuration from the environment: always a string, possibly absent; convert and default at the
  boundary, fail with a message that names the variable

## Reproduce

```bash
cd /tmp && python -c "import sys; sys.path.insert(0, '$OLDPWD/labs/lab13_environment/buggy'); import calibrate; print(calibrate.calibrate(500))"; cd -
python -m pytest labs/lab13_environment -q
```

## Diagnose

Three bugs, three environments. For each, write down *what is different* between the machine where it
works and the one where it fails. That difference is the bug: not the code, the assumption the code
makes about its surroundings.

## Fix

1. Remove the `yaml` import. The settings file can be JSON (standard library), or the import can be
   guarded (`try: import yaml except ImportError: yaml = None`) with a clear error when the feature is
   used without it. Do not add a dependency for one optional file.
2. `CALIBRATION_FILE = Path(__file__).resolve().parents[3] / "datasets" / "clean" / "calibration.csv"` -
   relative to the file, not to wherever the user happened to be.
3. `tolerance_from_env` returns `float(os.environ.get("PRESSURE_TOLERANCE", "5.0"))` and raises
   `ValueError("PRESSURE_TOLERANCE must be a number, got 'two'")` on bad input.

## Prevent recurrence

A clean clone must work: CI installs *only* `pip install -e ".[dev]"` and runs the tests from the repository
root and from a temporary directory. Every dependency is declared; every path is relative to `__file__` or
passed in; every environment variable is read in one place with a default and a conversion. The reference
`cli.py` takes the path as an argument for exactly this reason.

## Hint ladder

1. For each failure, which of the three (package, cwd, variable) is it? The exception type tells you.
2. `python -c "import calibrate; print(calibrate.__file__)"` shows where the module is; where is the data
   relative to that?
3. The tests show the expected default (5.0) and the expected message.

## Deliverable

`calibrate.py` with the tests green from any directory, and one sentence per bug naming the assumption
the original code made about its environment.
