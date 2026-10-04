# Chapter 12 · Working like a professional: bug reports, postmortems and the capstone

*For the capstone (lab 12).*

## A bug report someone can act on

Half of debugging in a team is communicating the bug well enough that someone else can reproduce it.
The template in `.github/ISSUE_TEMPLATE/bug_report.md` asks for exactly what a debugger needs, in order:

1. **Symptom, verbatim.** The last line of the traceback, the wrong number, the duration. Not "it
   crashes" but `KeyError: 'threshold'`; not "it is slow" but "the monthly job took 11 minutes; last
   release it took 2 seconds".
2. **Reproduction.** The exact command and the input. If the input is a file, attach it or name it. A
   bug with a reproduction is half fixed; a bug without one is a rumour.
3. **Actual versus expected.** What happened and what should have happened - and *why you think so*: a
   docstring, a test, a specification, last week's report.
4. **Environment.** Python version, OS, package version (`pip show engdebug`).
5. **Your hypothesis**, if you have one, and what you have tried.

The same discipline applies to asking for help in a chat or a forum: the smallest complete example
that shows the problem (a *minimal reproducible example*), what you expected, what you got, what you
tried. Building that example finds the bug yourself about half the time.

## Reading an incident

An incident is a bug with consequences: the report was wrong for a week, the batch job missed its
window, the operator was not alerted. The response has a shape that is worth learning on a simulated one
(the capstone) before meeting a real one:

1. **Triage.** What is affected, how badly, since when? Which incident first? (The one costing the most
   now - not the easiest.)
2. **Stabilise.** If the broken release can be rolled back, roll it back; fix on a branch.
3. **Reproduce** each incident with a command. Record it.
4. **Diagnose** with the workflow of chapter 1 - and with the version history: `git log` and `git diff`
   between the last good release and the bad one is often the fastest diagnostic there is. "What
   changed?" is the first question.
5. **Fix** with one commit per incident, each with its regression test.
6. **Verify** with the acceptance tests and the reproducing commands.
7. **Write the postmortem.**

## The postmortem

`docs/incident_postmortem_template.md`. The sections that matter most:

- **Root cause** - the line, the change, and the causal chain from change to symptom. If you cannot write
  the chain ("the encoding was changed to `utf-8` → the BOM became part of the first header name →
  `timestamp` was not found → `IngestionError: missing columns"), you have not found the cause.
- **Detection gap** - why did the tests, lint, types and monitoring not catch it? This is where the
  lasting value is. The capstone's three incidents each had a gap: no test loaded a BOM file (though one
  sat in `datasets/corrupted/`), the only drift test used a positive drift, and there was no performance
  test at all.
- **Prevention** - concrete, with owners: the regression test added (by name), the rule turned on, the
  review practice. "Be more careful" is not a prevention.

Postmortems are **blameless**. The question is never "who did this?" but "what let this through?" - a
team that punishes mistakes stops reporting them, and unreported bugs are the expensive kind.

## Reviewing a fix

The reviewer's checklist for a pull request that claims to fix a bug:

- Does the description name a root cause, with a chain?
- Is there a test that fails on the old code and passes on the new? (Check out the old code and run it.)
- Does the diff touch only what the fix needs? A "fix" that also reformats three files hides what changed.
- Are the error messages and names clear to someone who was not there?
- Did the detection gap get closed, or just this instance of it?

## The capstone

`capstone/README.md` is the brief: a release candidate with three open incidents, acceptance tests that
fail, two weeks. Everything in chapters 1-11 is in it: a byte-order mark (chapter 4), a dropped `abs()`
(chapter 5), a quadratic loop (chapter 9), `git diff` against the last release (chapter 10), one commit
per fix with its test (chapter 2), and a postmortem (this chapter). The grading rubric in
`docs/rubrics.md` weights the *process* and the *root cause* above the fix itself, because the fix is the
part that transfers least to the next bug.

## Habits this chapter starts

- **Report bugs the way you would want to receive them**: symptom, reproduction, expected, environment.
- **"What changed?" before "what is wrong?"** The diff is the first diagnostic.
- **One commit per incident, one test per commit.**
- **Write the postmortem while it is fresh, and make the detection gap the longest section.**
- **Blameless.** Find what let it through, fix that.

This is the end of the course's chapters. The labs are the course; the chapters only explain them.
