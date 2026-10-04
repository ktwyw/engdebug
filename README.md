<div align="center">

# engdebug

**Testing, debugging and optimising Python code, for engineers: a sensor-data pipeline that works, thirteen labs where it is deliberately broken, and the tests, tools and habits that find the bugs and keep them found.**

[![tests](https://github.com/ktwyw/engdebug/actions/workflows/tests.yml/badge.svg)](https://github.com/ktwyw/engdebug/actions/workflows/tests.yml)
[![labs](https://img.shields.io/badge/labs-13%20incl.%20capstone-orange)](labs)
[![error sources](https://img.shields.io/badge/error%20sources-20%2B-blue)](docs/error_catalog.md)
[![python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](pyproject.toml)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0000--0002--8488--9833-a6ce39)](https://orcid.org/0000-0002-8488-9833)

</div>

Most programming courses teach you to write code. This one teaches the half of the job that comes after:
reading a traceback, reproducing a failure, finding the line that caused it (not the line where Python
noticed), fixing it with the smallest change, and writing the test that keeps it fixed. It is built for a
*Programming for Engineers* course and for anyone learning Python who has written a few hundred lines
and met their first `KeyError`.

The setting is a small industrial system: a pipeline that reads sensor files from two pumps, validates
them, computes efficiency, drift and anomaly scores, raises alerts and writes a daily report. The
reference version in `src/engdebug/` works and is tested at every level. The labs in `labs/` hand you
broken copies of it with a realistic story - the report that showed 0.0 for a week, the file that "looks
the same", the monitor that is "intermittent", the monthly job that now takes minutes - and a test file
that fails until you have found the cause.

```bash
git clone https://github.com/ktwyw/engdebug && cd engdebug
pip install -e ".[dev]"
python -m pytest -q                                   # the reference pipeline: all green
python -m engdebug.cli datasets/corrupted/sensor_day1_corrupted.csv    # see what good error handling looks like
python -m pytest labs/lab01_tracebacks -q             # your first lab: five failing scripts
```

## The course: chapters, labs, habits

Thirteen chapters in [`docs/course/`](docs/course) explain every concept from zero - what a traceback is
and how to read one, what a test is and how `pytest` runs it, how exceptions travel, why `0.1 + 0.2` is
not `0.3`, why a default `[]` is shared, what a logger is, how to read a profile, what a virtual
environment protects you from - each with a runnable example in [`examples/`](examples) and ending with
the programming habits it starts. The labs practise the chapters on broken code, and
[`docs/habits.md`](docs/habits.md) collects the habits with the chapter and lab that build each. The
intended path for self-study is chapter → lab → notes, in order; [`docs/course/00_getting_started.md`](docs/course/00_getting_started.md)
is the first step and takes fifteen minutes.

## The labs

Every lab has the same shape, which is the debugging workflow itself: **context → reproduce → observe →
diagnose → fix → prevent recurrence → deliverable**. Each is a `README.md` handout, a `buggy/` folder you
edit, and a test file that goes green when you are done. Worked solutions are in `solutions/`.

| # | Lab | What breaks | What you learn |
|---|---|---|---|
| 01 | [Traceback triage](labs/lab01_tracebacks) | five scripts, five error classes | reading tracebacks; `SyntaxError`, `NameError`, `TypeError`, `IndexError`, `AttributeError`/`KeyError` |
| 02 | [Unit test rescue](labs/lab02_unit_testing) | an inverted formula, wrong precedence, no guards | pytest; normal/boundary/error tests; tests as specification |
| 03 | [Exception design](labs/lab03_exceptions) | bare excepts that turned a missing file into a mean of 0.0 | handle vs raise; custom exceptions; context; chaining; never print |
| 04 | [Dirty data](labs/lab04_data_validation) | BOM, CRLF, placeholders, decimal commas, two date formats, duplicates, impossible values | input contracts; repair vs reject; reporting every skipped row |
| 05 | [Logic bugs](labs/lab05_logic_bugs) | six functions that run and are all wrong | boundary denominators, off-by-one, units, float `==`, `>=`, misplaced powers; known-answer tests |
| 06 | [Class design](labs/lab06_class_design) | pump 2 shows pump 1's readings; `fault → running` | mutable defaults, class vs instance state, invariants, `__eq__`/`__hash__` |
| 07 | [Integration failure](labs/lab07_integration) | two modules that each pass their own tests | interface contracts; integration tests at the boundary; config drift |
| 08 | [Logging](labs/lab08_logging) | the "intermittent" monitor | the `logging` module; levels; diagnosing by logs; `dict.get` and `except: pass` as silent failures |
| 09 | [Profiling](labs/lab09_profiling) | a month that takes minutes | `perf_counter`, `cProfile`, reading a profile, the hidden O(n²) |
| 10 | [Optimisation with proof](labs/lab10_optimization) | the same, made fast | running statistics, grouping once; equivalence tests; before/after benchmarks |
| 11 | [CI and quality](labs/lab11_ci_quality) | three red jobs | `ruff`, `mypy --strict` (a type error that is a logic error), pull requests |
| 12 | [Capstone](capstone) | release candidate 0.2.0-rc1: three incidents | the whole workflow under pressure; a postmortem |
| 13 | [Environment](labs/lab13_environment) | works on my machine | undeclared dependencies, cwd-relative paths, environment variables as strings |

`python tools/check_labs.py` proves that every lab's broken code fails its tests and every solution
passes them ([`docs/LAB_STATUS.md`](docs/LAB_STATUS.md)); it runs in CI, so the labs cannot drift.

## What is covered

**Error sources** (one example of each in [`docs/error_catalog.md`](docs/error_catalog.md)): syntax and
indentation; name and scope; type; attribute, key, index; value; zero division; file, permission and
encoding; import and environment; recursion and memory; assertion; and the ones with no traceback -
logic (boundaries, off-by-one, units, floating point, comparison operators), state (mutable defaults,
shared class attributes, missing invariants), integration (contract drift), silent failures (swallowed
exceptions, harmless defaults), performance (the wrong complexity, repeated work), and environment
(works on my machine).

**Debugging tools**: [`docs/debugger_walkthrough.md`](docs/debugger_walkthrough.md) covers post-mortem `pdb`,
`breakpoint()`, conditional breakpoints, `pytest --pdb`, and the same operations in VS Code and PyCharm.

**Code testing and debugging**: classes of test (unit, integration, end-to-end, regression, smoke,
performance, acceptance) and approaches (example-based, boundary, parametrised, property-based with
Hypothesis, black/white-box, error-case) in [`docs/testing_guide.md`](docs/testing_guide.md); the
seven-step debugging workflow and the tools for each situation (`pdb`/`breakpoint()`, `-X dev`, logging,
profilers) in [`docs/debugging_workflow.md`](docs/debugging_workflow.md); structured JSON logging with a run id (`--json-logs`); exceptions, assertions and
error messages in lab 03 and throughout `src/engdebug/exceptions.py`.

**Efficiency and optimisation**: measure first (`perf_counter`, `timeit`, `cProfile`, `tracemalloc`,
scaling tests), the usual causes in order of payoff, proving equivalence, reporting - in
[`docs/performance_playbook.md`](docs/performance_playbook.md) and labs 09-10.

**Industrial relevance**: CI across three operating systems and four Python versions with lint, type
checks, tests and the lab checker; issue and pull-request templates that ask for reproduction steps and
root cause; structured logging; versioned clean and corrupted datasets; a release-candidate incident with
a [postmortem template](docs/incident_postmortem_template.md) and a worked example.

## For instructors

[`docs/syllabus.md`](docs/syllabus.md) lays the labs over twelve weeks with deliverables, grading weights
and a before/after plan for measuring impact (time to root cause, first-fix success rate, regression
rate, confidence); [`docs/rubrics.md`](docs/rubrics.md) gives the learning outcomes and a four-level rubric
on six criteria; [`docs/course_checklist.md`](docs/course_checklist.md) lists what is covered and what is
left for a second edition. To distribute without answers, delete `solutions/` (the CI lab job will then
report the missing solutions; disable it or keep a private copy).

## For self-learners

Start with [chapter 0](docs/course/00_getting_started.md). Then, for each lab: read its chapter (30-45
minutes), do the lab (60-90 minutes), write a page of notes in your own words. Every chapter is written
for someone who has never seen the concept; every lab handout links to its chapter and lists the habits
it practises. Open `solutions/` only after your tests are green or after an honest hour with all three
hints used. Everything runs with Python 3.10+ and `pytest`; nothing needs an account or a GPU. The whole
course is about forty hours.

## Repository layout

```
docs/course/         13 chapters: the concepts, from zero, one per lab
docs/habits.md       the programming habits the course builds, with the chapter and lab for each
examples/            one runnable script per chapter
labs/lab01..lab13/   handout (links to its chapter), buggy/ code, failing tests, hint ladder
solutions/           worked solutions with notes; the capstone's fixed release and postmortem
capstone/            release candidate 0.2.0-rc1 with three incidents, acceptance tests
src/engdebug/        the reference pipeline (standard library only) with a reading guide
tests/               unit, integration, e2e, regression (one per lab), performance
datasets/            clean/ and corrupted/ sensor files, documented fault by fault
docs/                workflow, error catalog, testing guide, performance playbook, debugger walkthrough, postmortem template, syllabus, rubrics, checklist
tools/               make_datasets.py, check_labs.py
.github/             CI workflow, issue and pull-request templates
```

## Author

**Yanwei Wang** - personal open-source project.
[GitHub @ktwyw](https://github.com/ktwyw) · [ORCID 0000-0002-8488-9833](https://orcid.org/0000-0002-8488-9833) ·
wangyanwei@gmail.com

Also by the author: [engbayesopt](https://github.com/ktwyw/engbayesopt), [engdoe](https://github.com/ktwyw/engdoe),
[engregress](https://github.com/ktwyw/engregress), [engstoch](https://github.com/ktwyw/engstoch), [englincontrol](https://github.com/ktwyw/englincontrol),
[engnumeric](https://github.com/ktwyw/engnumeric), [engmolines](https://github.com/ktwyw/engmolines), [engmath](https://github.com/ktwyw/engmath),
[engstat](https://github.com/ktwyw/engstat), [fluidmech](https://github.com/ktwyw/fluidmech), [engrheo](https://github.com/ktwyw/engrheo),
[engthermo](https://github.com/ktwyw/engthermo), [engcolloid](https://github.com/ktwyw/engcolloid), [engdiscrete](https://github.com/ktwyw/engdiscrete),
[engreact](https://github.com/ktwyw/engreact), [engsep](https://github.com/ktwyw/engsep) and [engbalance](https://github.com/ktwyw/engbalance).

## License

MIT - see [LICENSE](LICENSE). Contributions welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).
