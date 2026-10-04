# Labs

Fourteen guided labs including a capstone. Lab 14 (engineering correctness) belongs right after lab 05 in the suggested order. Every lab follows the same shape, which is the debugging workflow
itself: **context → reproduce → observe → diagnose → fix → prevent recurrence → deliverable**.

Each lab directory holds a `README.md` handout, a `buggy/` folder with the broken code (edit it in place),
and a `test_labNN.py` that fails at the start and passes when the lab is done:

```bash
python -m pytest labs/lab03_exceptions -q
```

Worked solutions are in `solutions/labNN/` (instructors may remove that directory before distributing).
`python tools/check_labs.py` verifies that every lab's buggy code fails its tests and every solution passes.

| Lab | Topic | Error sources |
|---|---|---|
| 01 | Traceback triage | SyntaxError, NameError, TypeError, IndexError, AttributeError/KeyError |
| 02 | Unit test rescue | inverted formula, wrong operator order, missing guards |
| 03 | Exception design | bare except, swallowed errors, print instead of raise, no context, no chaining |
| 04 | Dirty data | BOM, CRLF, header case, blank lines, placeholders, decimal comma, second date format, duplicates, impossible values, unknown units |
| 05 | Logic bugs | boundary denominator, off-by-one, unit mix-up, float equality, >= vs >, misplaced power |
| 06 | Class design | mutable default, class vs instance attribute, missing invariants, unchecked state transitions, eq without hash |
| 07 | Integration | interface contract mismatch, renamed config key, errors reported far from their cause |
| 08 | Logging | dict.get with a harmless default, except-pass, case-mismatched keys; diagnosing by logs |
| 09 | Profiling | hidden O(n²), repeated work, string concatenation; cProfile and perf_counter |
| 10 | Optimisation | running statistics, grouping once, join; proving equivalence and measuring speed-up |
| 11 | CI and quality | unused imports, import order, long lines, a type error that is a logic error, an empty-input crash |
| 12 | Capstone | a broken release with a logic bug, a data-handling bug and a performance regression |
| 14 | Engineering correctness | wrong units (cP, Celsius, percent), wrong equations (a missing /2, a missing g, a flipped log), correlations outside their range, silent extrapolation, an unvalidated property; verification and validation |
| 13 | Environment | an undeclared dependency, a cwd-relative path, an environment variable read as a string without a default |

Suggested pace: one lab per week, labs 09-10 together, lab 13 with lab 11, the capstone over two weeks. See
`docs/syllabus.md`.
