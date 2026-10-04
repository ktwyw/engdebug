# Lab 11 · Industrial workflow: make the CI green

**Context.** `quality.py` was pushed on Friday afternoon. The CI pipeline has three jobs - lint, type
check, tests - and all three are red. The author is on holiday. You are the reviewer.

**Time.** 60 minutes. **Prerequisites.** Labs 01-07; `pip install ruff mypy pytest`.

## What you will learn

- what a CI pipeline is: the same three commands you can run locally, run automatically on every push
- static analysis: `ruff` finds unused imports, wrong import order, over-long lines and bugs that need no
  execution; `mypy --strict` finds a function whose annotation says `int` while it returns a `float`
- that lint and type errors are often *real* bugs wearing a tidy uniform: here the type error is the test
  failure
- the pull-request discipline: one fix per commit, a message that says *why*, tests as evidence

## Reproduce

```bash
ruff check --isolated --select E,F,W,I,B --line-length 120 labs/lab11_ci_quality/buggy/quality.py
mypy --strict labs/lab11_ci_quality/buggy/quality.py
python -m pytest labs/lab11_ci_quality -q
```

Three tools, three reports. Read all three before fixing anything; some findings are the same bug seen
from different angles.

## Diagnose

- **ruff**: two unused imports (F401) and import order (I001), a line over 120 characters (E501).
- **mypy**: `hours_between` is annotated `-> int` but returns `delta.total_seconds() / 3600`, a `float`.
  That is not pedantry: the docstring says "whole hours", the test expects 2 for 2 h 45 min, and the report
  prints "2.75 h 45 min". The type checker found the logic bug.
- **tests**: `hours_between` (above), `shift_for` at 22:00 (`elif hour < 22` makes 22:00 "night" - check
  the test's expectation and the docstring, and decide which is right), `report([])` crashes on
  `min([])`.

## Fix

Make each job green in turn, committing after each with a message like `fix: hours_between returns whole
hours (int) as documented`. Do not silence a tool to make it pass (`# noqa`, `# type: ignore`) unless you
can write one sentence justifying it in the comment.

## Prevent recurrence

The three commands live in `ci.yml` and in a `pre-commit` hook, so nobody can push red. The reference
repository's `.github/workflows/tests.yml` runs them on every push across Python versions; the issue and
pull-request templates in `.github/` ask for reproduction steps and test evidence. Read them; you will use
them in the capstone.

## Hint ladder

Use one hint at a time, only after an honest attempt.

1. Run the three commands locally, in the order lint, types, tests; read all three reports before fixing anything.
2. mypy's complaint about `hours_between` is a logic bug: 'whole hours' means `int(... // 3600)`.
3. `min([])` raises; guard `report` for an empty list.

## Deliverable

`quality.py` with all three jobs green, and a pull-request description written with
`.github/pull_request_template.md`: what was wrong (root cause, not symptom), what changed, how you
verified it.
