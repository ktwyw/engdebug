# Runnable examples

One small script per chapter where a concept is best seen by running it. Each file says how to run it
at the top; none needs anything beyond the course's `pip install -e ".[dev]"`. `tests/e2e/test_examples.py`
runs them all in CI so they cannot rot.

| file | shows |
|---|---|
| `ch01_traceback.py` | a traceback whose cause is two frames above where it is raised (run under `pdb`) |
| `ch02_first_test.py` | a function with its normal, boundary and error tests; run with pytest |
| `ch03_exceptions.py` | try/except/else, a custom exception with context, `raise ... from` |
| `ch04_csv_pitfalls.py` | the byte-order mark, CRLF and a decimal comma; the right `open()` |
| `ch05_floats.py` | `0.1 + 0.2`, a boundary denominator, a unit mix-up |
| `ch06_mutable_default.py` | the shared default list and class attribute, proved with `is` |
| `ch08_logging.py` | logging levels; a silent default made visible |
| `ch09_profile.py` | a quadratic loop, its linear fix, the scaling test |
