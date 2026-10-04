# Course checklist

## A. Must-have (core release) - all present

**Learning and assessment**
- [x] learning outcomes covering debugging, testing, exceptions, optimisation and the industrial workflow (`docs/rubrics.md`)
- [x] a rubric with four performance levels on six criteria (`docs/rubrics.md`)
- [x] pre/post impact metrics: time to diagnose, first-fix success, regression rate, test quality, confidence (`docs/syllabus.md`)

**Technical scope** (one lab and one catalog entry each; `docs/error_catalog.md`)
- [x] syntax and indentation (lab 01)
- [x] runtime exceptions: TypeError, ValueError, KeyError, IndexError, AttributeError, ZeroDivisionError (labs 01-03)
- [x] logic bugs: wrong formula, precedence, boundary denominator, off-by-one, units, float equality, comparison operators (labs 02, 05)
- [x] data and I/O bugs: missing fields, malformed values, placeholders, path, encoding, line endings (labs 03, 04)
- [x] OOP and state bugs: mutable defaults, class vs instance attributes, missing invariants, equality/hash (lab 06)
- [x] environment, import and configuration bugs: undeclared dependency, cwd-relative path, environment variables, config key drift (labs 07, 08, 13)
- [x] performance: quadratic algorithms, repeated work, string building; memory per record with `tracemalloc` (labs 09-10)
- [x] exceptions and assertions: hierarchy, context, chaining, when to assert (lab 03, `docs/testing_guide.md`)
- [x] error-message interpretation and traceback reading (lab 01, `docs/debugging_workflow.md`)

**Testing coverage** (`tests/`, `docs/testing_guide.md`)
- [x] unit, integration, regression (one per lab), end-to-end (through the CLI), performance
- [x] boundary and edge cases in every unit test file; parametrised tests; property-based tests with Hypothesis

- [x] thirteen concept chapters for self-study (`docs/course/`), each from zero, with runnable examples (`examples/`, run in CI)
- [x] a catalogue of programming habits with the chapter and lab that build each (`docs/habits.md`); every lab names the habits it practises

**Debugging workflow habits**: reproduce, minimise, observe, hypothesise, instrument, fix and verify, prevent - the structure of every handout.

**Efficiency and optimisation**: baseline first (lab 09), `cProfile`/`timeit`/`perf_counter`/`tracemalloc`, correctness-preserving optimisation proven by an equivalence test (lab 10), before/after evidence in `benchmark.md`.

**Industrial relevance**: CI with tests, ruff, mypy and the lab checker across 3 OS x 4 Python versions; PR template (root cause, fix, evidence, detection gap); bug-report template (repro, actual vs expected, environment); an incident capstone with a postmortem template and a worked example.

## B. Nice-to-have

- [x] `pdb` and IDE debugger walkthrough (`docs/debugger_walkthrough.md`)
- [x] property-based testing with Hypothesis (`tests/unit/test_calculations.py`)
- [x] static typing: the package passes `mypy` in default mode; lab 11 uses `--strict` on one module - the progression a team would follow
- [x] structured JSON logging with a run id (`logsetup.configure(json_lines=True)`, `--json-logs`)
- [ ] security-minded checks (`bandit`, input hardening) - second edition
- [ ] concurrency / async debugging lab - second edition
- [ ] a small observability dashboard or metrics export - second edition

## C. Quality gate

- [x] 13 labs run end to end without instructor patching: `python tools/check_labs.py` (buggy fails, solution passes, for every lab; `docs/LAB_STATUS.md`)
- [x] all starter tests and CI pass on a clean clone (`pip install -e ".[dev]" && python -m pytest`)
- [x] each lab has an objective, a failing case, a hint ladder, a solution with notes, and a regression test in `tests/regression/`
- [x] the capstone has three bug types (data handling, logic, performance) and a 100x performance regression
- [ ] grading rubric tested on sample submissions - an instructor action before the first cohort; `solutions/` plus one deliberately weak submission per lab is the suggested calibration set

## D. Tooling

`pytest`, `hypothesis`, `ruff`, `mypy`, `cProfile`/`timeit`/`tracemalloc` (standard library), GitHub Actions.
