# Lab 03 · Exception design: stop swallowing errors

**Context.** Last Tuesday's report showed a mean temperature of 0.0 for pump 1. Nobody noticed for a
week. The loader had caught every error, printed "could not load file" to a terminal nobody was watching,
and returned an empty list; `mean_reading` then caught the `ZeroDivisionError` and returned 0.0. Two
`except:` clauses turned a missing file into a plausible number.

**Time.** 60 minutes. **Prerequisites.** Labs 01-02.

## What you will learn

- why a bare `except:` (or `except Exception: pass`) is the most expensive line in a code base
- the difference between an error you can *handle* (retry, skip with a warning, use a default) and one you
  must *raise* (the caller has to know)
- how to define an exception hierarchy (`LoaderError` → `BadRowError`) so that callers can catch what they
  mean
- `raise ... from exc` to keep the original traceback attached
- why error messages carry the file, the row and the value: a message without context is a message you
  will have to reproduce

## Reproduce

```bash
python -c "import sys; sys.path.insert(0, 'labs/lab03_exceptions/buggy'); import loader; print(loader.mean_reading('does_not_exist.csv'))"
python -m pytest labs/lab03_exceptions -q
```

A file that does not exist has a mean reading of 0.0. That is the bug.

## Diagnose

Read `loader.py` and list every place an error can occur (opening the file, a missing column, a reading
that is not a number, an empty file) and what the code currently does with each. For each, decide:
handle or raise? What would the *caller* want to know?

## Fix

1. Define `class LoaderError(Exception)` and `class BadRowError(LoaderError)` at the top of the module.
2. `load` raises `LoaderError` for a missing file (message includes the path) and a missing `reading`
   column (message names the column); it raises `BadRowError` for an unparseable reading with the row
   number and the offending value, chained to the original `ValueError` with `raise ... from exc`.
3. `mean_reading` raises `LoaderError("... no readings ...")` for an empty file instead of returning 0.
4. Remove every `print`. Library code never prints; it raises or logs (lab 08).

The tests spell out the messages they expect. A good message answers "what, where, which value" in one
line.

## Prevent recurrence

`ruff` reports bare excepts (rule E722) and `except Exception: pass` (B001/BLE001 in some configurations).
Turn the rule on and the code review becomes automatic. The reference package's `exceptions.py` is the
same idea at full size: a `PipelineError` base, one subclass per stage, every message with context.

## Hint ladder

Use one hint at a time, only after an honest attempt.

1. `grep -n except loader.py` - how many of them name an exception type?
2. What does `mean_reading('nope.csv')` return? What should the caller see instead?
3. Define the two classes first; then make every `except` either re-raise one of them with context or disappear.

## Deliverable

The fixed `loader.py` (tests green) and a short note: one paragraph on what "could not load file" cost the
plant, and the rule you propose for when code may catch an exception without re-raising it.
