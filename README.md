<div align="center">

# engdebug

### The half of programming nobody teaches: finding the bug, proving the fix, and knowing the number is right.

**A complete, self-contained course in testing, debugging and optimising Python for engineers** -
fourteen chapters that explain every concept from zero, fourteen labs on a realistic sensor pipeline
that is deliberately broken, an incident-response capstone, and the engineering discipline of units,
ranges, verification and validation that no traceback will ever enforce for you.

[![tests](https://github.com/ktwyw/engdebug/actions/workflows/tests.yml/badge.svg)](https://github.com/ktwyw/engdebug/actions/workflows/tests.yml)
[![chapters](https://img.shields.io/badge/chapters-14-blueviolet)](docs/course)
[![labs](https://img.shields.io/badge/labs-14%20incl.%20capstone-orange)](labs)
[![error sources](https://img.shields.io/badge/error%20sources-25%2B-blue)](docs/error_catalog.md)
[![python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](pyproject.toml)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0000--0002--8488--9833-a6ce39)](https://orcid.org/0000-0002-8488-9833)

</div>

---

> *Last Tuesday's report showed a mean temperature of 0.0 for pump 1. Nobody noticed for a week. The
> loader had caught every error, printed "could not load file" to a terminal nobody was watching, and
> returned an empty list. Two `except:` clauses turned a missing file into a plausible number.*
> — Lab 03

> *The plant replaced a sizing spreadsheet with `pipeflow.py`. Its pressure drops are twice too high, its
> gas volumes a hundred times too small, its pump powers off by a factor of ten. Every function returns a
> plausible-looking number.*
> — Lab 14

Programming courses teach you to write code that works. This course teaches what happens after: the
traceback at 3 a.m., the report that is quietly wrong, the job that took two seconds last month and times
out now, the correlation used in a regime it was never fitted for. Every lab starts with a story like
the two above, hands you the broken code, and does not let you off until the tests are green and you can
say *why* it was wrong and *what* now prevents it.

## Who it is for

- **Students in a Programming for Engineers course** - the chapters are the lectures, the labs are the
  assignments, the rubrics and syllabus are in `docs/`.
- **Anyone learning Python** who has written a few hundred lines and met their first `KeyError` - the
  course is self-contained: Python 3.10+, `pytest`, and about forty hours.
- **Engineers who already code** and want the testing, profiling, V&V and CI habits of professional
  software work, learned on problems that look like theirs (sensor data, pipe flow, pumps, heat
  exchangers), not on to-do apps.

## What you will be able to do

| after | you can |
|---|---|
| chapter 1 and lab 01 | read a traceback bottom-up and top-down, and find the line that *caused* the error, not the one that reported it |
| chapters 2-3, labs 02-03 | write the three tests every function needs; design exceptions a person can act on at 3 a.m. |
| chapters 4-6, labs 04-06 | handle a file that "looks the same" and is not; find the formula that is wrong without a traceback; fix the class that shares state between instances |
| chapters 7-8, labs 07-08 | find the bug at the boundary between two modules that each pass their tests; diagnose an "intermittent" failure from its logs |
| chapter 9, labs 09-10 | profile a program, fix the line that owns 93 % of the time, and prove the output did not change |
| chapters 10-11, labs 11, 13 | make a red CI pipeline green; make code work on a machine that is not yours |
| chapter 13, lab 14 | catch a viscosity in the wrong unit, an equation missing its ½, a correlation outside its range - and keep the verification and validation record that says why a number can be trusted |
| chapter 12, the capstone | respond to three incidents in a broken release, one commit and one regression test each, and write a blameless postmortem |

## Start here

```bash
git clone https://github.com/ktwyw/engdebug && cd engdebug
python -m venv .venv && source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python -m pytest -q                                      # the reference pipeline: all green
python -m pytest labs/lab01_tracebacks -q                # your first lab: five failing scripts
```

Then read [chapter 0](docs/course/00_getting_started.md) (fifteen minutes) and work the course in order:
**read the chapter, do the lab, write a page of notes**. Every lab handout links to its chapter and
names the habits it practises; every chapter has a runnable example in [`examples/`](examples).

## The course

| # | chapter | lab | the story |
|---|---|---|---|
| 0 | [Getting started](docs/course/00_getting_started.md) | - | your environment, the three rules, a notes file |
| 1 | [How Python fails](docs/course/01_how_python_fails.md) | [01 Traceback triage](labs/lab01_tracebacks) | five scripts, five error classes |
| 2 | [Testing from zero](docs/course/02_testing_from_zero.md) | [02 Unit test rescue](labs/lab02_unit_testing) | the efficiency that "looks wrong" |
| 3 | [Exceptions](docs/course/03_exceptions.md) | [03 Exception design](labs/lab03_exceptions) | the report that showed 0.0 for a week |
| 4 | [Data](docs/course/04_data.md) | [04 Dirty data](labs/lab04_data_validation) | the file that "looks the same" |
| 5 | [Logic and numbers](docs/course/05_logic_and_numbers.md) | [05 Logic bugs](labs/lab05_logic_bugs) | six functions that run and are all wrong |
| 13 | [Engineering correctness](docs/course/13_engineering_correctness.md) | [14 Units, equations, ranges, V&V](labs/lab14_engineering_correctness) | the spreadsheet replacement that is off by 2, 9.8, 100, 273 and 1000 |
| 6 | [Classes and state](docs/course/06_classes_and_state.md) | [06 Class design](labs/lab06_class_design) | pump 2 shows pump 1's readings |
| 7 | [Modules and contracts](docs/course/07_modules_and_contracts.md) | [07 Integration failure](labs/lab07_integration) | two modules that each pass their own tests |
| 8 | [Logging](docs/course/08_logging.md) | [08 Logging](labs/lab08_logging) | the "intermittent" monitor |
| 9 | [Performance](docs/course/09_performance.md) | [09 Profiling](labs/lab09_profiling), [10 Optimisation](labs/lab10_optimization) | the month that takes minutes |
| 10 | [Tools and workflow](docs/course/10_tools_and_workflow.md) | [11 CI and quality](labs/lab11_ci_quality) | three red jobs |
| 11 | [Environments](docs/course/11_environment.md) | [13 Environment](labs/lab13_environment) | works on my machine |
| 12 | [Working like a professional](docs/course/12_working_like_a_professional.md) | [12 Capstone](capstone) | release candidate 0.2.0-rc1, three incidents |

Every lab has the same shape - **context → reproduce → observe → diagnose → fix → prevent recurrence →
hint ladder → deliverable** - because that shape *is* the debugging workflow. Worked solutions with notes
are in [`solutions/`](solutions); `python tools/check_labs.py` proves that every lab's broken code fails
its tests and every solution passes them, and runs in CI so the labs cannot drift.

## What is covered

**Error sources** - all with a minimal example, cause, fix and lab in [`docs/error_catalog.md`](docs/error_catalog.md):
syntax and indentation · name and scope · type · attribute, key, index · value · zero division · file,
permission, encoding · import and environment · recursion and memory · assertion · **logic** (boundaries,
off-by-one, floating point, operators) · **state** (mutable defaults, shared class attributes, missing
invariants) · **integration** (contract drift) · **silent failures** (swallowed exceptions, harmless defaults)
· **performance** (the wrong complexity) · **environment** (works on my machine) · **units** · **equations**
· **ranges of validity** · **validation**.

**Testing and debugging** - classes of test (unit, integration, end-to-end, regression, smoke,
performance, acceptance, **benchmark**) and approaches (example-based, boundary, parametrised,
property-based with Hypothesis) in [`docs/testing_guide.md`](docs/testing_guide.md); the seven-step
workflow in [`docs/debugging_workflow.md`](docs/debugging_workflow.md); `pdb`, `breakpoint()` and the IDE
in [`docs/debugger_walkthrough.md`](docs/debugger_walkthrough.md); exceptions, assertions and messages
throughout.

**Verification and validation** - units in every name, SI inside, conversion at the boundary; analytical
limits, identities, scaling laws and independent methods for every equation; ranges enforced in code;
benchmarks whose expected values name a source outside the code; the V&V record. In
[`docs/verification_and_validation.md`](docs/verification_and_validation.md), `src/engdebug/engineering.py`
and `tests/benchmarks/`.

**Efficiency** - measure first (`perf_counter`, `timeit`, `cProfile`, `tracemalloc`), fix the complexity,
prove equivalence, report before/after, in [`docs/performance_playbook.md`](docs/performance_playbook.md).

**Industrial practice** - CI on three operating systems and four Python versions with tests, `ruff`, `mypy`
and the lab checker; issue and pull-request templates that ask for reproduction and root cause; structured
logging; versioned clean and corrupted datasets; a release-candidate incident with a
[postmortem template](docs/incident_postmortem_template.md) and a worked example.

**Habits** - forty-odd, each tied to the chapter and lab that builds it, in [`docs/habits.md`](docs/habits.md).

## For instructors

[`docs/syllabus.md`](docs/syllabus.md) lays the chapters and labs over twelve to thirteen weeks with
deliverables, grading weights and a before/after plan for measuring impact (time to root cause, first-fix
success rate, regression rate, confidence). [`docs/rubrics.md`](docs/rubrics.md) gives learning outcomes
and a four-level rubric on six criteria; [`docs/course_checklist.md`](docs/course_checklist.md) records
what is covered and what a second edition would add. To distribute without answers, delete `solutions/`
and disable the `labs` CI job in the students' copy.

## Repository layout

```
docs/course/         14 chapters, from zero, one per lab
docs/habits.md       the programming habits the course builds, by chapter and lab
examples/            one runnable script per chapter (executed in CI)
labs/lab01..lab14/   handout (links to its chapter), buggy/ code, failing tests, hint ladder
solutions/           worked solutions with notes; the capstone's fixed release and postmortem
capstone/            release candidate 0.2.0-rc1 with three incidents, acceptance tests
src/engdebug/        the reference pipeline + engineering calculations (standard library only), with a reading guide
tests/               unit, integration, e2e, regression (one per lab), performance, benchmarks (V&V)
datasets/            clean/ and corrupted/ sensor files, documented fault by fault
docs/                workflow, error catalog, testing guide, V&V guide, performance playbook, debugger walkthrough,
                     postmortem template, syllabus, rubrics, checklist
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
