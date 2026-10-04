# Chapter 3 · Exceptions, assertions and error messages

*For lab 03. Runnable example: `examples/ch03_exceptions.py`.*

## What an exception is

When a function cannot do its job it does not return a value; it *raises* an exception: an object that
carries a type (`ValueError`), a message, and a record of where it happened. Raising stops the function
at that line. The exception then travels up the call stack - through the function that called it, and
the one that called that - until some `try` block catches it or it reaches the top and the program
prints the traceback and exits.

This is the mechanism that makes "fail loudly" possible: a problem deep inside a library can stop the
whole program with a precise report, instead of returning a nonsense value that is used for a week.

## The four parts of `try`

```python
try:
    f = open(path)                 # the code that might fail
except FileNotFoundError as exc:   # runs only if that TYPE of exception was raised
    raise LoaderError(f"cannot open {path}") from exc
else:                              # runs only if no exception was raised
    data = f.read()
finally:                           # runs always, exception or not (cleanup)
    f.close()
```

- `except SomeType as exc` catches exceptions of that type *and its subclasses* (chapter 1's families).
  You can list several: `except (ValueError, KeyError)`.
- `else` is for code that should run only after success - keeping it outside the `try` means an
  exception *in it* is not accidentally caught by the same `except`.
- `finally` is for cleanup; in practice `with open(...) as f:` does the closing for you and `finally` is
  rare.

## Handle, or raise?

Every `except` is a decision: *this function knows what to do about this problem*. Three honest options:

1. **Recover.** Retry a network call; use a default when a config key is absent *and a default is
   genuinely acceptable*; skip a malformed row *and report it*. The program continues and the user is told.
2. **Translate.** Catch a low-level exception and raise one that means something at this level, with
   context: `FileNotFoundError` becomes `IngestionError("datasets/day1.csv: file not found")`. Keep the
   original attached with `raise ... from exc`.
3. **Let it pass.** Do not catch it at all. If this function cannot do anything useful about the
   problem, the caller might, or the user should see it. Not catching is a valid - often the best -
   choice.

What is never right is the fourth option: catch it and pretend it did not happen.

```python
try:
    readings.append(float(row["reading"]))
except:
    pass
```

This line turns a corrupted file into a shorter list, silently. Lab 03's story - a week of reports
showing 0.0 - is this line plus one more like it. A bare `except:` also catches `KeyboardInterrupt`
(you cannot stop the program with Ctrl-C) and `SystemExit`. Rules:

- name the exception type you expect, and only that type;
- do something visible: re-raise, raise a better one, log a warning, or return a value whose meaning
  the caller cannot confuse with success;
- never `except: pass`, never `except Exception: pass`, never return `0`, `[]` or `None` to mean
  "something went wrong" unless the docstring says so and the caller checks.

## Raising your own

`raise ValueError("...")` for an argument that is wrong; `raise TypeError` for a wrong type; `raise
KeyError` for a missing key. Choose the built-in type whose meaning matches so that callers can reason
about it.

**The message is for the person at 3 a.m.** It must say *what* went wrong, *where* (file, row, field) and
*which value*:

```python
raise ValueError(f"input power must be positive, got {input_kw}")
raise IngestionError(path, f"missing reading {text!r}", row=row_number)
```

`{value!r}` shows the repr, so an empty string appears as `''` and a string with a space as `' 6.25'` -
the difference between a clear report and an hour of confusion.

## Custom exceptions

A package defines its own exception classes so that callers can catch *what they mean*:

```python
class PipelineError(Exception):
    """Everything this package raises on purpose."""

class IngestionError(PipelineError): ...
class ValidationError(PipelineError): ...
```

Now `except PipelineError` catches every deliberate failure of the pipeline and nothing else - a
`TypeError` from a genuine bug still escapes with its traceback, as it should. Subclasses can carry
structured context (`exc.row`, `exc.field`) for callers that want it; the message carries it for humans.

## Chaining: keep the original

```python
try:
    value = float(text)
except ValueError as exc:
    raise BadRowError(path, row, text) from exc
```

`from exc` stores the original in `__cause__`, and the traceback shows both: your context on top of
Python's reason. Without `from`, Python still shows both (with "During handling of the above exception,
another exception occurred") but that wording suggests an accident; `from` says it was deliberate.
`from None` hides the original when it adds nothing.

## EAFP and LBYL

Two styles for conditions that may fail. *Look before you leap*: check first.

```python
if "reading" in row and row["reading"] != "":
    value = float(row["reading"])
```

*Easier to ask forgiveness than permission*: try it and catch the failure.

```python
try:
    value = float(row["reading"])
except (KeyError, ValueError) as exc:
    ...
```

Python favours EAFP: the operation itself is the check, there is no gap between checking and doing, and
the exception's message says exactly what was wrong. LBYL is better when the check is cheap and the
failure expensive, or when you want to validate everything before doing anything (chapter 4).

## Assertions

`assert condition, "message"` raises `AssertionError` if the condition is false. It is for
**invariants**: things that cannot be false if your code is correct, checked during development.

```python
def moving_average(values, window):
    assert window >= 1, "callers must validate window"   # a contract between you and yourself
```

It is **not** for validating input from users, files or the network, because `python -O` strips every
`assert` from the program. Data validation is an `if` that raises `ValueError`; an assertion is a note
that says "if this fails, I have a bug, not bad data". Use assertions freely inside algorithms (the
running variance is never negative; the list is sorted after sorting) and never at the boundary.

## Error messages people can act on

Compare:

- `Error` - nothing.
- `invalid value` - what value? where?
- `could not convert string to float: 'N/A'` - Python's; good.
- `sensor_day1.csv, row 19: missing reading 'N/A'` - yours; better: the file, the row, the value, and
  the word "missing" that tells the operator what to look for.

The test for a message: could someone fix the data or the config from the message alone, without
reading the code? If not, add the missing piece.

## Habits this chapter starts

- **Fail loudly.** A wrong answer is worse than no answer. Code that cannot do its job raises.
- **Catch what you name, name what you catch.** Every `except` has a type and a visible consequence.
- **Context in every message.** What, where, which value.
- **Define your package's exceptions on day one.** A base class and a subclass per stage; it costs ten
  lines and makes every caller's `except` meaningful.
- **Assertions for invariants, exceptions for input.**

Next: [Chapter 4 · Data: files, encodings and validation](04_data.md).
