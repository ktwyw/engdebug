# The debugging workflow

Seven steps. Every lab in this repository walks through them in order; after lab 03 you should be able
to run them without the handout.

| step | what you do | what you write down |
|---|---|---|
| 1. Reproduce | find a command that fails the same way every time | the command, the exact output |
| 2. Minimise | shrink the input and the code path until the failure is as small as possible | the smallest failing case |
| 3. Observe | read the traceback bottom-up (what) then top-down (where); read the logs; read the data | exception type, file:line, the values involved |
| 4. Hypothesise | one sentence: "the cause is X because Y" | the hypothesis, and what would disprove it |
| 5. Instrument | a print, a log line, `breakpoint()`, a profiler - to test the hypothesis, not to wander | the evidence |
| 6. Fix and verify | the smallest change; rerun the reproducing command | the diff, the before/after output |
| 7. Prevent | a regression test, an assertion, a type hint, a lint rule, a log line | the test's name |

## Reading a traceback

```
Traceback (most recent call last):
  File "run.py", line 14, in main            <- outermost call: where you started
    found = analyse.alerts(records, CONFIG)
  File "analyse.py", line 19, in alerts      <- innermost: where Python noticed
    limit = config["threshold"][rec["unit"]]
KeyError: 'threshold'                        <- what went wrong: read this line FIRST
```

Bottom line: the exception type and message. Then walk up: the innermost frame is where the error was
*raised*; the cause may be several frames up (lab 07: a `TypeError` in `analyse` caused by `ingest`).
`raise ... from exc` adds a second traceback above with "The above exception was the direct cause".

## The error classes you will meet

See `docs/error_catalog.md` for one example of each with its usual cause and fix. In order of how often
beginners meet them: `SyntaxError`, `NameError`, `TypeError`, `AttributeError`, `KeyError`, `IndexError`,
`ValueError`, `ZeroDivisionError`, `ImportError`/`ModuleNotFoundError`, `FileNotFoundError`,
`UnicodeDecodeError`, `RecursionError`, `MemoryError` - and then the ones with no traceback at all:
logic errors, silent failures, performance.

## Tools, by situation

- a crash with a traceback: read it; `python -X dev` for extra warnings; `python -m pdb script.py` or
  `breakpoint()` on the line before the crash, then `p variable`, `u`/`d` to move between frames
- wrong numbers, no crash: known-answer tests (lab 05); print the intermediate values at one point
- "it works on my machine": `pip list`, Python version, `locale`, the exact file bytes (`od -c | head`)
- it does nothing: logging at INFO with counts per stage (lab 08)
- it is slow: `cProfile` first, then `timeit` on the suspect (lab 09); never guess
- it is flaky: fix the seed, pin the dependency versions, look for shared state (lab 06) and time/order
  dependence

## Habits that make debugging rare

Small functions; tests written with the code; assertions for invariants (`assert window >= 1` during
development, an explicit `ValueError` in production code the user can reach); specific exceptions with
context; no bare `except`; logging instead of print; a linter and a type checker in CI; a regression test
for every bug you fix - the test is the bug's gravestone.
