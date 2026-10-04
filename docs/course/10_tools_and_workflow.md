# Chapter 10 · Tools and workflow: git, linters, types, the debugger and CI

*For lab 11. See also `docs/debugger_walkthrough.md`.*

## Version control: git in the amount you need

Git records snapshots of your files so that you can see what changed, go back, and work with others
without emailing zip files. The five commands that cover a course:

```bash
git status                       # what has changed since the last snapshot
git add labs/lab05_logic_bugs/buggy/analysis.py
git commit -m "fix: moving_average divides by the number of values present at the start"
git log --oneline                # the history
git diff                         # what you changed and have not committed
```

A **commit** is a snapshot with a message. Make them small - one fix, one commit - and write the message
as the sentence you would say to a colleague: *what* changed and *why* ("fix: hours_between returns whole
hours (int) as documented"), not "fixed bug" or "changes". Six months later the message is all you have.

A **branch** is a line of work; `main` is the one that is always green. Work on a branch
(`git switch -c fix-moving-average`), commit, and merge back when the tests pass. On GitHub the merge
is a **pull request**: the diff plus a description, reviewed by someone before it lands. The
description has the same three parts as a bug fix: what was wrong (root cause), what changed, how it was
verified. `.github/pull_request_template.md` is the form.

When a bug fix lands, the regression test lands in the same commit. A commit that says "fix" with no
test is a commit that should be questioned in review.

## Linters: errors without running

A linter reads your code and reports problems a compiler would catch in another language: undefined
names, unused imports and variables, a comparison that is always true, a mutable default, a bare
`except`, an `f`-string with nothing in it. `ruff` does this in milliseconds:

```bash
ruff check .                     # report
ruff check . --fix               # fix what is safe to fix (unused imports, import order)
ruff format .                    # consistent formatting, so diffs show changes and not style
```

Every finding is a question: "did you mean this?" Most are real mistakes wearing a tidy uniform. Lab 11's
unused `timedelta` import is harmless; its undefined name would have been a `NameError` at 2 a.m. Turn
the linter on in the editor and the questions arrive as you type.

## Type hints and `mypy`

```python
def hours_between(a: datetime, b: datetime) -> int:
```

Type hints are documentation Python does not enforce - but `mypy` does. It reads the hints and checks
that every call and return is consistent:

```
quality.py:30: error: Incompatible return value type (got "float", expected "int")
```

That is not pedantry: the docstring says *whole hours*, the function returns `2.75`, and the report
prints "2.75 h 45 min". The type checker found a logic bug. Hints also make the contract (chapter 7)
checkable: if `load` says `-> list[dict]` and starts returning a dict, `mypy` complains in the consumer.

Start with hints on every function signature (parameters and return). Run `mypy` in default mode; move
to `--strict` module by module as the code base matures (lab 11 does it on one module). `Optional[T]`
(or `T | None`) on anything that can be `None` forces callers to handle it - which is most of the
`'NoneType' object has no attribute` errors removed at a stroke.

## The debugger

`print` shows you one value at one place. The debugger stops the program and lets you look at everything.

```bash
python -m pdb script.py arg      # then: c (continue to the crash), bt (stack), p var, u (up a frame), q
```

Or put `breakpoint()` on a line and run normally; execution pauses there with `n` (next line), `s`
(step into), `p` (print), `c` (continue). `python -m pytest --pdb` drops into the debugger at the first
failing assertion. In VS Code, click left of a line number, press F5, and the Variables and Call Stack
panels are `p` and `bt` with a mouse. `docs/debugger_walkthrough.md` has a full session on lab 07's crash.

Use the debugger when you need to see *several* values at once or walk *up* the stack to find where a
wrong value came from; use logging (chapter 8) when the problem happens on the 1 400th row or in a run
you cannot reproduce at your desk.

## Continuous integration

CI runs the same three commands - tests, lint, types - on a clean machine every time code is pushed,
and refuses to merge a pull request that fails. The point is not the automation; it is the *clean
machine*: no files you forgot to commit, no packages you installed and forgot, no "works on my
machine". `.github/workflows/tests.yml` runs the reference tests on three operating systems and four
Python versions, plus `ruff`, `mypy` and the lab checker.

Reading a CI failure is the same as reading a traceback: find the first red job, open its log, read the
last lines, reproduce locally with the same command. Fix it in a commit that says why. Do not silence
the tool (`# noqa`, `# type: ignore`, `@pytest.mark.skip`) to turn the job green unless you can write one
sentence in the comment justifying it - and then write that sentence.

## Code review

Reading someone else's change before it merges is the most effective bug-finding activity known, and
the best way to learn. Review for: does the description name a root cause? is there a test that fails
without the fix? does the change touch only what the fix needs? are the names and messages clear to
someone who was not there? A review comment is a question, not a verdict.

## Habits this chapter starts

- **Commit small, with a message that says why.**
- **`ruff check` and `python -m pytest -q` before every commit; the editor runs them as you type.**
- **Type hints on every signature; `mypy` in CI.**
- **A failing test for every bug, in the same commit as the fix.**
- **Never silence a tool without a one-sentence justification in the code.**
- **Reproduce CI failures locally with the same command.**

Next: [Chapter 11 · Environments and configuration](11_environment.md).
