# Chapter 1 · How Python fails: errors, exceptions and the traceback

*For lab 01. Runnable example: `examples/ch01_traceback.py`.*

## What happens when you run a program

Python reads your file top to bottom and does two things: first it *parses* the whole file into
instructions (if the text is not valid Python it stops here, before running anything), then it *executes*
the instructions one at a time, line by line, calling functions when it meets a call and returning when
they finish.

Keep this picture; it explains the two families of error.

**Errors before execution.** `SyntaxError` and `IndentationError` are found while parsing. Nothing in the
file has run yet - not even the `print("starting")` on line 1. That is why a syntax error on line 40 stops
a program that "worked yesterday": the parser rejects the whole file.

**Errors during execution: exceptions.** Everything else happens while running. Python reaches a line,
tries to do what it says, and cannot: the name does not exist, the types do not fit, the index is past
the end. It creates an *exception* object describing the problem and stops the current function. If the
function that called it does not handle the exception (chapter 3), it stops too, and so on up to the top
of the program, which prints a traceback and exits.

## Anatomy of a traceback

```
Traceback (most recent call last):
  File "run.py", line 14, in <module>
    main("day2.csv")
  File "run.py", line 9, in main
    found = alerts(records, CONFIG)
  File "analyse.py", line 19, in alerts
    limit = config["threshold"][rec["unit"]]
KeyError: 'threshold'
```

Read it in this order:

1. **The last line first.** `KeyError: 'threshold'` - the type of the problem and its message. The type
   tells you *what kind* of thing went wrong; the message tells you *which* (here: which key was missing).
2. **The frame just above it.** `analyse.py, line 19, in alerts`, with the line of code. This is where
   Python *noticed* the problem - the line that was executing when the exception was raised.
3. **Upwards from there.** Each `File ...` line is a function that was waiting for the one below it.
   `main` called `alerts`; the top-level program (`<module>`) called `main`. This chain is the *call
   stack*; "most recent call last" means the innermost call is at the bottom.

Beginners read the first line and the last line and stop. The middle matters because **the line where
the error is raised is often not the line that caused it**. In the traceback above, `config` has no
`'threshold'` key - but the dictionary was built in `main` (or earlier) and `alerts` only revealed it.
Lab 07 has a `TypeError` raised in one module whose cause is a return statement in another.

When one exception causes another you see two tracebacks joined by *"The above exception was the direct
cause of the following exception"*; read the top one for the original cause.

## The error classes you will meet

Each entry: what Python is telling you, the usual cause, the usual fix.

**`SyntaxError`** - the text is not valid Python. A missing colon after `def`/`if`/`for`, an unclosed
bracket or quote, `=` where `==` was meant inside a condition, Python 2's `print x`. The caret (`^`)
points near the problem, sometimes a line *after* it (an unclosed bracket is noticed on the next line).
Fix: read the line before the caret too. **`IndentationError`** is its cousin: mixed tabs and spaces,
or a block that is not indented. Set your editor to insert spaces.

**`NameError: name 'valeu' is not defined`** - you used a name Python has never seen: a typo, a variable
defined in another function, or something used before the line that defines it. Fix: spell it the same
way everywhere (the linter catches this before you run anything).

**`TypeError`** - the operation does not fit the type: `71.2 > "120"` (a number against a string),
`len(5)`, calling a function with the wrong number of arguments, `None + 1`. The classic source is data
that arrives as text - from a file, a config, a web form, `input()` - and is compared or added without
conversion. Fix: convert at the boundary where the text enters the program (`float(...)`), once.

**`AttributeError: 'str' object has no attribute 'uppercase'`** - the object has no method or field by
that name. Either the name is wrong (`upper`, not `uppercase`) or the object is not what you think: the
most common form is `'NoneType' object has no attribute ...`, meaning something returned `None` where you
expected a real object (a function without a `return`, a lookup that found nothing).

**`KeyError: 'sensor'`** - the dictionary has no such key. Wrong spelling, wrong case, a key renamed in
one place but not the other, or - a favourite of lab 04 - a key that *looks* right but carries an
invisible character. Fix: print `d.keys()`; use `d.get(key, default)` when a missing key is a normal
situation and a clear error when it is not.

**`IndexError: list index out of range`** - you asked for position `n` of a list with `n` elements (the
last valid index is `n - 1`), or the list is empty. Off-by-one is the usual cause: `range(len(x))` with
`x[i + 1]` inside. Fix: iterate over the elements, not the indices, when you can.

**`ValueError`** - the type is right but the value is not acceptable: `float("N/A")`, `int("")`,
`math.sqrt(-1)`, `datetime.strptime` with a text that does not match the format. Fix: validate the value
before converting, and report *which* value was bad.

**`ZeroDivisionError`** - almost always an empty list (`sum(x) / len(x)`) or a quantity that is zero in
a situation nobody thought about (a stopped machine's input power).

**`FileNotFoundError`**, **`PermissionError`** - the path is wrong *relative to where the program is
running* (chapter 11), or the file is not where you think. Print `os.getcwd()` and the full path.
**`UnicodeDecodeError`** - you opened a file with the wrong encoding (chapter 4).

**`ModuleNotFoundError`**, **`ImportError`** - the package is not installed *in the environment you are
running* (the virtual environment is not activated, or it was installed elsewhere), or the module name is
wrong, or two modules import each other in a circle.

**`RecursionError`** - a function calls itself without a stopping condition. **`MemoryError`** - you
built something far larger than you meant to (a matrix of 14 400 x 14 400 to read its diagonal).

And then the ones **without a traceback**, which are the subject of labs 05-10: the formula that is
wrong, the error that was caught and ignored, the program that is correct and far too slow. The
traceback is the easy case; a program that runs and lies is the hard one.

## Reading the message, not just the type

`KeyError: 'threshold'` tells you the key. `ValueError: could not convert string to float: 'N/A'` tells
you the value. `TypeError: '>' not supported between instances of 'float' and 'str'` tells you both types.
Python's messages are specific; read every word before forming a theory. When *your* code raises an
error (chapter 3), hold it to the same standard: the message says what, where and which value.

## A method, before any tool

When something fails, before you touch the code:

1. Read the last line of the traceback. Say the error class out loud and what it means in general.
2. Find the innermost frame. Look at the line. Which name, index, key or value is involved?
3. Ask: is the cause on this line, or did this line only reveal it? If the value is wrong, where did it
   come from? Walk up the stack.
4. Write a one-sentence hypothesis: "the cause is X because Y".
5. Test the hypothesis with the cheapest check: a `print`, a `breakpoint()` (chapter 10), running the
   one line in the interactive prompt.
6. Fix. Rerun the command that failed. Then write the test (chapter 2).

Lab 01 gives you five scripts to practise exactly this.

## Habits this chapter starts

- **Run early, run often.** Write five lines, run them. A syntax error in five new lines is found in
  seconds; in two hundred, in an afternoon.
- **One name, spelled one way.** Choose descriptive names (`input_kw`, not `x`) and let the editor's
  autocomplete repeat them; most `NameError`s are typos in names chosen too hastily to remember.
- **Convert at the boundary.** Text from files, configs and users becomes numbers *once*, where it
  enters the program, in a function whose only job is that conversion.
- **The linter before the interpreter.** `ruff check .` finds undefined names, unused imports and a
  dozen other mistakes without running anything. Run it before every commit; let the editor run it as
  you type.

Next: [Chapter 2 · Testing from zero](02_testing_from_zero.md).
