# Lab 01 · Traceback triage

**Context.** Five short scripts from the plant's analysis folder, each written in a hurry, each failing.
Your job is not to rewrite them; it is to read the traceback, find the one line that is wrong, fix it, and
say what *class* of error it was.

**Time.** 60 minutes. **Prerequisites.** None.

## What you will learn

- how to read a Python traceback from the bottom up (the exception), then from the top down (the call chain)
- the five most common error classes: `SyntaxError`, `NameError`, `TypeError`, `IndexError`, and the
  `AttributeError`/`KeyError` pair
- that the line in the traceback is where Python *noticed* the problem, which is not always where it was caused

## Reproduce

```bash
python labs/lab01_tracebacks/buggy/script1_syntax.py
python labs/lab01_tracebacks/buggy/script2_name.py
# ... and so on
python -m pytest labs/lab01_tracebacks -q      # all five checks fail at the start
```

## Observe

For each script, write down three things before changing anything:

1. the exception type and message (the last line of the traceback);
2. the file and line number Python points at;
3. your one-sentence hypothesis of the cause.

Script 3 deserves a second look: the comparison `71.2 > "120"` raises in Python 3, but in Python 2 it
silently returned a nonsense answer. A config file always hands you *strings*; the bug is a missing
conversion, not a missing comparison.

## Diagnose and fix

Fix each script with the smallest change that makes it correct. Do not add try/except: these are bugs, not
conditions to tolerate. The checks in `test_lab01.py` state the expected output.

## Prevent recurrence

For each script, name the habit that would have prevented the bug:

- script 1: run the file before committing; an editor with syntax highlighting
- script 2: a linter (`ruff check`) flags undefined names before you run anything
- script 3: convert config values at the boundary where they enter the program, and type-annotate
- script 4: loop over `range(len(x) - 1)` or, better, over `zip(x, x[1:])`
- script 5: `dict.get` with a clear default, or a `KeyError` that names the available keys

## Hint ladder

Use one hint at a time, only after an honest attempt.

1. Read the last line of the traceback first; it names the error class.
2. The line number points at where Python noticed; for script 4, what is the value of `i` on the last iteration?
3. Script 3: `type(config['high_limit'])`. Script 5: `record.keys()` and `dir(str)`.

## Deliverable

The five fixed scripts (tests green) and a half-page "traceback checklist" in your own words - the
steps you will follow next time a script crashes. Keep it; you will use it in every later lab.
