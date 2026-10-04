# Chapter 8 · Logging and observability

*For lab 08. Runnable example: `examples/ch08_logging.py`.*

## Why not `print`?

`print` is the first debugging tool everyone learns and it is fine for a script you run by hand and
delete. For anything that runs unattended - a nightly job, a pipeline, a library someone else imports -
it fails on four counts: you cannot turn it off without editing the code; you cannot turn it *on* in
production when something goes wrong; it goes to standard output, mixed with the program's real output
(the report), with no timestamp and no indication of where it came from; and library code that prints
pollutes every program that uses it.

The `logging` module fixes all four. It costs one import and one line per module.

## The model

- A **logger** is where your code sends messages. One per module: `log = logging.getLogger(__name__)`.
  `__name__` is the module's dotted name (`engdebug.pipeline`), so every message says where it came
  from, and loggers form a tree: configuring `engdebug` configures `engdebug.pipeline` too.
- A **level** says how important a message is: `DEBUG < INFO < WARNING < ERROR < CRITICAL`. The logger
  drops messages below its configured level, so DEBUG lines cost nothing when you are not looking.
- A **handler** says where messages go: the console, a file, a socket. **Formatters** say what a line
  looks like.
- **Configuration happens once, at the top of the program** (`main`, the CLI), never in library code.
  The library emits; the application decides what to show.

```python
# in a library module
import logging
log = logging.getLogger(__name__)

def load(path):
    ...
    log.info("loaded %d records from %s", len(records), path)
    log.warning("skipped row %d: %s", row, reason)

# in the application's main()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(name)s: %(message)s")
```

Note the `%d`/`%s` style: `log.info("loaded %d records", n)`, not `log.info(f"loaded {n} records")`. The
message is formatted only if it will be shown, so DEBUG lines do not pay for string formatting when DEBUG
is off.

## What to log at which level

| level | meaning | examples |
|---|---|---|
| DEBUG | every decision, for when you are diagnosing | the limit looked up for a unit; the z-score of each point |
| INFO | the milestones a reader needs to follow a normal run | "loaded 1728 records", "9 alerts", "report written to ..." |
| WARNING | something was skipped, defaulted or unusual, but the run continues | "skipped row 19: missing reading", "no limit configured for unit 'psi'" |
| ERROR | a step failed; the result is incomplete | "cannot open file", the exception that stopped a stage |
| CRITICAL | the program cannot continue | rare in this kind of code |

`log.exception("failed to load %s", path)` inside an `except` block logs at ERROR *with the traceback*.

The most useful lines are the INFO lines with counts: `loaded 1728 records`, `0 rows skipped`,
`2 records rejected`, `9 alerts`. When "it did nothing" happens, the count that is zero or missing
names the stage.

## Observability: diagnosing without reproducing

Lab 08's monitor fails on some days and not others. Nobody can reproduce it at a desk, and reading the
code did not find it. The method that does:

1. Add DEBUG lines that print the *decision inputs* in the suspect loop: the unit, the limit found for it,
   the reading.
2. Replace every `except ...: pass` with a WARNING that names the item and the exception.
3. Add INFO counts at every stage.
4. Run on the day that fails with `level=DEBUG` and *read the log*.

The DEBUG line shows `limit inf` for every `degC` reading - the lookup table's keys are in a different
case. The WARNING shows `S102: KeyError` - a sensor missing from the references, which the bare except
had hidden. Two bugs, found by making the program describe itself. That is what observability means: a
program you can see into after the fact. The DEBUG lines stay in the code at DEBUG level; they cost
nothing and they are there for next time.

## The two silent patterns

- `table.get(key, harmless_default)`: a missing key becomes a value that lets the code continue
  (`float("inf")` as a limit means "never alert"). Use `.get` only when the default is *genuinely correct*;
  otherwise look up with `[]` and let the `KeyError` speak, or check and WARN.
- `except Exception: pass` (or `except: continue`): the error is discarded. At minimum:
  `log.warning("%s: %s", item, exc)`.

A linter flags the second (E722, and B-rules for `pass` in excepts). Only reading flags the first.

## Structured logs

For logs that machines will search, one JSON object per line (`logsetup.configure(json_lines=True)`,
`--json-logs` on the CLI) with a run id lets you `grep` a run, count warnings by type, or feed a log
aggregator. The content is the same; only the format changes. For a course project, the human format is
enough; know that the other exists and costs one formatter.

## Testing logs

`caplog` captures log records in a test:

```python
def test_unknown_unit_is_warned(caplog):
    with caplog.at_level(logging.WARNING):
        threshold_alerts([{"unit": "psi", ...}])
    assert any("psi" in m for m in caplog.messages)
```

A test that a warning is emitted is a test that the failure is *visible* - the property lab 08 is about.

## Habits this chapter starts

- **`log = logging.getLogger(__name__)` at the top of every module; configure once in `main`.**
- **Library code never prints.** It returns, raises or logs.
- **A count per stage at INFO.** The cheapest observability there is.
- **A WARNING for every skip, default and ignored error.**
- **DEBUG lines for decision inputs**, left in place.
- **Read the log before reading the code**, when the failure is "it did nothing".

Next: [Chapter 9 · Performance](09_performance.md).
