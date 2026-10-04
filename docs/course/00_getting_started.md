# Chapter 0 · Getting started, and how to use this course

This course assumes you can write a Python function with a loop, a list and a dictionary, and that you
have met your first `KeyError`. It does not assume you have ever written a test, read a traceback to the
end, or used a debugger. Every chapter teaches a concept from zero, then a lab asks you to use it on
realistic broken code.

## Set up once

**1. Python.** You need Python 3.10 or newer. Open a terminal and check:

```bash
python --version        # or: python3 --version
```

If that prints 3.9 or older, install a current Python from python.org (Windows/macOS) or your package
manager (Linux). On some systems the command is `python3`; use whichever prints 3.10+.

**2. A copy of the course.**

```bash
git clone https://github.com/ktwyw/engdebug
cd engdebug
```

(No git? Download the ZIP from GitHub and unpack it. Chapter 10 explains git; you do not need it to start.)

**3. A virtual environment.** This is the single most important habit in this chapter. A virtual
environment is a private folder of installed packages for *this* project, so that what you install here
cannot break another project, and what another project installed cannot break this one.

```bash
python -m venv .venv                 # create it (once)
source .venv/bin/activate            # macOS/Linux: activate it (every new terminal)
.venv\Scripts\activate               # Windows (PowerShell or cmd)
```

Your prompt now starts with `(.venv)`. Everything you `pip install` goes into `.venv/`. Chapter 11
explains why this matters so much; for now, trust it.

**4. Install the course package and its tools.**

```bash
pip install -e ".[dev]"
```

`-e` means *editable*: Python imports the code from `src/engdebug/` directly, so edits take effect
without reinstalling. `[dev]` pulls in the tools: `pytest` (testing), `hypothesis` (property tests),
`ruff` (linter), `mypy` (type checker).

**5. Check that everything works.**

```bash
python -m pytest -q
```

You should see a row of dots and `passed`. That is the reference pipeline's test suite: the working
version of the code the labs break. If this fails, something in steps 1-4 went wrong; the most common
cause is a Python older than 3.10 or a terminal where the virtual environment is not activated.

**6. An editor.** Any editor works; VS Code with the Python extension is free and shows errors as you
type, which is the cheapest debugging there is. Set it to use `.venv` as the interpreter (bottom-right
corner, "Select Interpreter"). Turn on *format on save* with `ruff` if you can; it removes a whole class
of arguments about style.

## How a lab works

Each lab lives in `labs/labNN_name/` with three things:

- `README.md` - the handout. It starts with a short story from an industrial setting, because that is
  how bugs arrive: not as "exercise 3b" but as "the report said 0.0 and nobody noticed for a week".
- `buggy/` - the broken code. You edit it in place.
- `test_labNN.py` - tests that fail until the bug is fixed. Run them with
  `python -m pytest labs/labNN_name -q`.

The handout always has the same sections, in this order, and the order is the point:

| section | what it asks of you |
|---|---|
| Context | read the story; what *should* the code do? |
| Reproduce | run the command; see the failure yourself |
| Observe | write down what you see *before* changing anything |
| Diagnose | find the cause (not the symptom) |
| Fix | the smallest change that makes it right |
| Prevent recurrence | the test, assertion, lint rule or habit that stops it coming back |
| Hint ladder | three hints, each more specific; use them one at a time |
| Deliverable | what to hand in (or, self-studying, what to write in your notes) |

Each lab has a chapter in `docs/course/` with the concepts it needs. **Read the chapter first**; the
handout assumes you have.

## The three rules

1. **Reproduce before you change.** A bug you cannot trigger on demand is a bug you cannot know you have
   fixed. The first thing you write down in any lab is the command that fails.
2. **Write it down.** The exception, the line number, your hypothesis. Debugging in your head loses the
   thread the moment you get interrupted; debugging on paper (or in a notes file) does not.
3. **The fix is not done until there is a test.** A bug fixed without a test is a bug on leave.

## Keep a notes file

Create `notes/` in your copy (it is in `.gitignore`, so it stays yours). One file per lab with: the
reproducing command, what you observed, your hypotheses (including the wrong ones), the fix, and one
sentence on the habit that would have prevented it. By lab 13 that file is your personal debugging
handbook, written in your own words - more useful than anything in this repository.

## If you are self-studying

Work the chapters and labs in order; each pair takes two to three hours. Solutions are in `solutions/`.
The honest rule: open a solution only when your tests are green (to compare) or after an hour of being
stuck with all three hints used. Reading a solution first teaches you what the answer *was*; finding it
teaches you how to find the next one, which is the only skill that transfers.

Next: [Chapter 1 · How Python fails](01_how_python_fails.md).
