# Capstone · Incident response: release candidate 0.2.0-rc1

**The situation.** Version 0.2.0-rc1 of the pipeline (`capstone/release/engdebug_release/`) was cut on
Friday. Over the weekend three incidents were raised:

- **INC-101** (ops): the March file that 0.1.0 processed with warnings is now rejected outright with
  `missing columns ['timestamp']`.
- **INC-102** (process engineer): sensor T102 has been drifting *down* for a week and no drift alert was
  raised; T101, drifting up, did alert.
- **INC-103** (scheduler): the monthly batch job that took two seconds now times out after ten minutes.

You are the on-call engineer. The acceptance tests in `capstone/tests/` fail on the release candidate.
Your job is to ship a fixed 0.2.0.

**Time.** Two weeks (about 8 hours). **Prerequisites.** All labs.

## Rules

1. Work on a copy: `cp -r capstone/release my_release` and point the tests at it with
   `ENGDEBUG_CAPSTONE_SRC=my_release python -m pytest capstone/tests -q`.
2. Reproduce each incident with a command before you touch the code; record the command.
3. One commit per incident; the message names the root cause, not the symptom.
4. Every fix comes with a regression test added to `capstone/tests/` (or your own test file) that fails
   on the release candidate and passes on your fix.
5. For INC-103, measure before and after (lab 09's `cProfile`, lab 10's benchmark table); "it is faster
   now" without numbers is not evidence.
6. Write the postmortem with `docs/incident_postmortem_template.md`: timeline, root cause, fix,
   detection gap (why did the tests of 0.1.0 not catch it?), prevention.

## What is being assessed

The rubric in `docs/rubrics.md`: debugging process (did you reproduce, isolate, hypothesise, verify),
root-cause analysis (the *cause*, with a causal chain from the change to the symptom), testing quality,
diagnostics, efficiency evidence, and professional practice (commits, PR description, postmortem).

## Hints, if stuck after an honest hour

- INC-101: lab 04. Look at the first three bytes of the file and at how it is opened.
- INC-102: lab 05. Compare the alert condition with the one for thresholds; what makes a drift "large"?
- INC-103: labs 09-10. Profile a day, then the month; the function at the top is small and looks
  harmless.

The reference solution is in `solutions/capstone/` with a worked postmortem; do not open it until your
pull request is written.
