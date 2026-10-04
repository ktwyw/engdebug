# Lab 07 · Integration failure: two modules that each pass their own tests

**Context.** Last sprint the ingestion stage was rewritten to return columns (a dict of lists) because
"pandas will want it that way". The analysis stage still expects rows (a list of dicts). Each module's
unit tests pass. The pipeline crashes on the first run, and when the first crash is fixed, a second one
appears: the config key was renamed in one place but not the other.

**Time.** 60 minutes. **Prerequisites.** Labs 01-06.

## What you will learn

- that unit tests prove each piece works alone and say nothing about whether the pieces fit
- *interface contracts*: what one module promises to return and the next one assumes it receives
- integration tests: a test that runs two stages together on real data, placed at the boundary
- how configuration drifts (`threshold` vs `thresholds`) and why a config schema belongs in one module

## Reproduce

```bash
python labs/lab07_integration/buggy/run.py datasets/clean/sensor_day2.csv
python -m pytest labs/lab07_integration -q
```

The first traceback is a `TypeError: string indices must be integers` deep inside `analyse.sensor_means` -
reported at the wrong place: the *cause* is in `ingest.load`.

## Diagnose

Print `type(records)` and `records.keys()` at the boundary. Iterating over a dict yields its keys
(strings), and `"timestamp"["sensor_id"]` is the error you saw. Then fix that and run again: `KeyError:
'threshold'`. Open `run.py` and `analyse.py` side by side.

## Fix

Choose and document the contract. The pragmatic choice is rows: `load` returns a list of dicts with
`timestamp`, `sensor_id`, `reading` (float), `unit`. (The columnar form can be derived in one line when
pandas is actually needed.) Then make the config key agree - `thresholds`, plural, in both places - and
make `alerts` raise a clear error naming the available keys when the config is missing one, instead of
a bare `KeyError`.

## Prevent recurrence

Write the integration test *at the boundary*: load a real file with `ingest.load` and pass the result to
`analyse.sensor_means`. Put the config schema in one module (`run.CONFIG` is the only definition) and have
the consumer validate it on entry. The reference `pipeline.py` + `tests/integration/test_pipeline.py`
show the full version: every stage on real data, clean and corrupted.

## Hint ladder

Use one hint at a time, only after an honest attempt.

1. Print `type(records)` right after `ingest.load` returns.
2. Iterating a dict yields its keys; `'timestamp'['sensor_id']` is the error you saw. Which module should change?
3. After that: `grep -n threshold *.py` - singular or plural?

## Deliverable

The fixed modules (tests green), the one-paragraph contract for `ingest.load` (what it returns, what it
raises), and a short note on who should have caught this - the author of the rewrite, the reviewer, or a
test that did not exist.
