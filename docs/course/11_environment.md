# Chapter 11 · Environments and configuration: "it works on my machine"

*For lab 13.*

## What "the environment" is

A program's behaviour depends on more than its source: on which Python runs it, which packages are
installed and in what versions, the current working directory, environment variables, the operating
system's conventions (path separators, line endings, default encoding), and the files that happen to be
on the disk. Two machines with the same source and different environments run different programs.
"Works on my machine" is the honest report of a bug in one of these.

## Packages and virtual environments

`pip install something` puts a package where the active Python looks for imports. If that is the
system Python, every project on the machine shares one set of packages, and project A's upgrade breaks
project B. A **virtual environment** (chapter 0) is a private set per project:

```bash
python -m venv .venv && source .venv/bin/activate     # create and activate
pip install -e ".[dev]"                               # install THIS project and its tools into it
pip list                                              # what is installed, with versions
```

`ModuleNotFoundError` on a machine where "it's installed" almost always means: installed in a different
environment than the one running the program. `python -c "import sys; print(sys.executable)"` tells
you which Python is running; `pip --version` tells you which environment `pip` targets. They must match.

## Declaring dependencies

Every package your code imports must be *declared* in `pyproject.toml`:

```toml
dependencies = []                                   # the pipeline needs only the standard library
[project.optional-dependencies]
dev = ["pytest>=7", "hypothesis>=6", "ruff>=0.4", "mypy>=1.5"]
```

A dependency you use but do not declare works on your machine (where you installed it by hand) and fails
on every other. Lab 13's `import yaml` is this bug. The choices when you want a package: declare it
(everyone gets it); make it optional and guard the import (`try: import yaml` / `except ImportError:
yaml = None`, with a clear error when the feature is used without it); or do without it (the standard
library's `json` reads a settings file just as well).

**Pinning.** `pytest>=7` says "at least 7"; for an application that must behave identically everywhere,
pin exact versions (`pip freeze > requirements.txt`) and install from that. For a library, loose bounds;
for a deployment, exact pins. Either way: a clean clone plus `pip install` must produce a working
program with nothing done by hand.

## The working directory

A relative path like `datasets/clean/calibration.csv` is resolved against the *current working
directory* - the folder the user was in when they typed `python`, which has nothing to do with where the
script lives. Run the same script from another folder and the file is "not found". Rules:

- paths to files that ship with the code are built from the file's own location:
  `Path(__file__).resolve().parent / "data" / "table.csv"`;
- paths to the user's files are *arguments* (the CLI takes the CSV path on the command line);
- never `os.chdir()` in library code;
- test from a different directory (`cd /tmp && python -m pytest /path/to/tests`) - CI does.

## Environment variables and configuration

`os.environ["PRESSURE_TOLERANCE"]` is a `KeyError` on any machine where the variable is not set, and a
string on every machine where it is. Configuration from the environment, a file, or the command line
arrives as text and may be absent; it is read in **one place**, with a default and a conversion, and a
message that names the variable when the value is bad:

```python
raw = os.environ.get("PRESSURE_TOLERANCE")
tolerance = float(default) if raw is None else float(raw)      # and a ValueError naming the variable on failure
```

Secrets (passwords, API keys) live in environment variables or a secrets store, never in the code or
the repository. A `.env` file that is in `.gitignore` is the usual local arrangement.

## Operating systems

Windows uses `\` in paths and `\r\n` line endings and may default to a non-UTF-8 encoding; macOS and
Linux differ in file-name case sensitivity. `pathlib.Path` handles the separators; `encoding=` and
`newline=` (chapter 4) handle the rest; CI on three operating systems handles the surprises. Python
versions differ too: a feature from 3.11 fails on 3.10 with an `AttributeError`, which is why
`requires-python` is declared and CI runs the versions you support.

## Reproducibility

The same program, the same data, the same answer - every time, on every machine. Beyond environments:
fix random seeds (`np.random.default_rng(2026)`; the course datasets are generated with one); never
depend on dictionary order from a set or on the time of day; keep the data that generated a result (the
course keeps every corrupted file that ever broke the parser); record versions. A result that cannot be
reproduced cannot be debugged.

## Habits this chapter starts

- **One virtual environment per project, activated before anything else.**
- **Every import declared; a clean clone must work.**
- **Paths from `__file__` or from arguments; never from the working directory.**
- **Configuration read once, converted once, defaulted once, with the variable named in every error.**
- **Seeds fixed; data versioned.**

Next: [Chapter 12 · Working like a professional](12_working_like_a_professional.md).
