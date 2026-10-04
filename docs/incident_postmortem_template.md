# Postmortem: <incident id and one-line title>

**Summary.** Two or three sentences: what broke, who noticed, how long it was broken, what fixed it.

## Timeline

- `YYYY-MM-DD HH:MM` - the change that introduced the problem (commit, release)
- `...` - first symptom observed (by whom, how)
- `...` - reproduced
- `...` - root cause identified
- `...` - fix deployed / tests green

## Symptom

What was observed, verbatim: the error message, the wrong number, the duration.

## Reproduction

The exact command and input that fail every time.

## Root cause

The *cause*, not the symptom: the line, the change, and the causal chain from change to symptom. One
paragraph. If you cannot write the chain, you have not found the cause.

## Fix

What changed (link the commit/diff). Why this is the smallest correct change.

## Detection gap

Why the existing tests, lint, types and monitoring did not catch it. This is the most useful section.

## Prevention

Concrete items with owners: the regression test added (name it), the lint/type rule turned on, the log
line added, the review rule, the dataset added to the integration suite.

## Lessons

One to three sentences, blameless: what the team learned, not who made the mistake.
