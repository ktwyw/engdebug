# Lab 08 · Logging and observability: the "intermittent" monitor

**Read first.** [Chapter 8 · Logging and observability](../../docs/course/08_logging.md) explains every concept this lab uses. **Habits practised:** logging, never print, in library code; a count per stage at INFO; a WARNING for every skip and default; read the log before the code (see [`docs/habits.md`](../../docs/habits.md)).


**Context.** The daily monitor is supposed to report pressure excursions and temperature drift. Some days
it reports nothing when the operators know something happened. There is no traceback, no message, no
clue; the script exits 0. The operators call it intermittent. It is not: it fails deterministically on
every day that has a temperature problem, and it has done so since the day the thresholds table was
"cleaned up".

**Time.** 60 minutes. **Prerequisites.** Labs 03 and 07.

## What you will learn

- the `logging` module: loggers, levels, a handler, a format with timestamps
- *observability*: a program that cannot be seen into cannot be debugged; logs are how a running program
  explains itself after the fact
- what to log at which level: DEBUG (every decision), INFO (milestones and counts), WARNING (something was
  skipped or defaulted), ERROR (a step failed)
- the two silent failure patterns here: `dict.get(key, harmless_default)` and `except Exception: pass`
- how to use logs to *find* a bug you cannot reproduce by reading

## Reproduce

```bash
python -c "import sys; sys.path.insert(0, 'labs/lab08_logging/buggy'); import monitor; print(monitor.run('datasets/clean/sensor_day2.csv'))"
python -m pytest labs/lab08_logging -q
```

Day 2 has a pressure excursion on P101 (reported) and a 4-degree drift on T101 (not reported). Nothing
says why.

## Diagnose with logging

Do not read for the bug yet. Add logging first:

1. at the top: `import logging` and `log = logging.getLogger(__name__)`;
2. in `threshold_alerts`, log at DEBUG the unit, the limit looked up and the reading for every record
   (temporarily), and at WARNING when a unit has no limit;
3. in `drift_alerts`, replace `except Exception: pass` with a WARNING that names the sensor and the
   exception;
4. in `run`, log at INFO how many records were loaded and how many alerts of each kind were found;
5. run with `logging.basicConfig(level=logging.DEBUG)` and read the output.

The DEBUG lines will show the limit for `degC` is `inf`. The WARNING will show which sensors have no
reference. Now you know both bugs without having read the code: the limits table has lower-case keys
(`degc`) while the data say `degC`, and S102 is missing from `REFERENCES` - which the bare except hid.

## What the log should look like when you are done

```
10:42:01 INFO     monitor: loaded 1728 records from datasets/clean/sensor_day2.csv
10:42:01 WARNING  monitor: no reference value for sensor S102: drift not checked
10:42:01 INFO     monitor: 6 threshold alerts
10:42:01 INFO     monitor: 1 drift alerts
10:42:01 INFO     monitor: 7 alerts in total
```

Every stage reports a count; every skip is a WARNING naming what was skipped. With `level=DEBUG` there
is one line per reading showing the unit, the limit and the value - the line that would have found the
case bug in a second.

## Fix

Make the unit lookup exact and loud (a missing limit is a configuration error worth a WARNING, not
`inf`), remove the bare except, keep the logging, delete the temporary DEBUG line or leave it at DEBUG
level where it costs nothing. Library code logs; it never prints.

## Prevent recurrence

Configuration tables are validated once at start-up against the units the data actually use. Every
`except` names the exception type and does something visible. A log line per stage with counts
(`loaded 1728 records, 9 alerts`) is cheap and makes "it did nothing" impossible: either the line is
there with the count, or the line is missing and you know which stage died. The reference `logsetup.py`
configures the format once; `pipeline.py` logs at every stage.

## Hint ladder

Use one hint at a time, only after an honest attempt.

1. Add `logging.basicConfig(level=logging.DEBUG)` and one `log.debug` with the unit, the limit and the reading inside the loop.
2. What limit does the DEBUG line show for `degC`? Compare the keys of `LIMITS` with the units in the file.
3. Replace `except Exception: pass` with `log.warning('%s: %s', sid, exc)` and read what it says.

## Deliverable

The fixed `monitor.py` (tests green), a sample of the log output from day 2, and a one-page diagnostic
playbook: *when the monitor reports nothing, check these three log lines*.
