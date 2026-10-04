## What was wrong

The root cause, not the symptom: the line, the change that introduced it, the causal chain to what users saw.

## What changed

One fix per PR where possible. Why this is the smallest correct change.

## How it was verified

- [ ] the reproducing command now passes: `...`
- [ ] a regression test was added: `tests/.../test_....py::test_...`
- [ ] `python -m pytest -q`, `ruff check`, `mypy` are green locally
- [ ] (performance changes) before/after timings:

## Detection gap

Why the existing tests did not catch this, and what now does.
