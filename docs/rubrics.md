# Learning outcomes and rubrics

## Learning outcomes

By the end of the course a student can:

1. interpret a Python traceback and locate the root cause of a crash;
2. classify a bug (syntax, runtime, logic, data, state, integration, performance, environment) and choose
   the matching diagnostic;
3. apply the seven-step workflow (reproduce, minimise, observe, hypothesise, instrument, fix and verify,
   prevent) without prompting;
4. write unit, integration, regression and performance tests with pytest, including boundary and error
   cases and at least one property-based test;
5. use exceptions and assertions appropriately: specific types, messages with context, chaining, no silent
   failures;
6. make a program observable with structured logging and diagnose a failure from its logs;
7. profile a program, read the profile, and optimise with evidence while proving the output unchanged;
8. work the way the industry works: CI with lint, type checks and tests; one fix per commit; a pull request
   with root cause and test evidence; a blameless postmortem.

## Rubric (four levels: 4 exemplary, 3 proficient, 2 developing, 1 beginning)

**A. Debugging process (25 %)**
4: reproduces reliably, minimises, states and tests hypotheses, verifies the fix with the reproducing command.
3: reproduces and fixes correctly with moderate structure. 2: fixes by trial and error, weak evidence.
1: cannot reproduce or justify the fix.

**B. Root-cause analysis (20 %)**
4: correct cause with a causal chain from change to symptom. 3: mostly correct, adequate explanation.
2: partial or mixed with symptoms. 1: incorrect or missing.

**C. Testing quality (20 %)**
4: regression tests for each bug plus boundaries and error cases; tests are small, named for the
behaviour, fail for one reason. 3: passing tests for the core behaviour. 2: few tests, no boundaries.
1: missing or failing.

**D. Exceptions, assertions, diagnostics (10 %)**
4: specific exceptions with context, assertions only for invariants, logging at the right levels.
3: mostly appropriate. 2: broad excepts or print debugging left in. 1: errors swallowed.

**E. Efficiency analysis and optimisation (15 %)**
4: profile-driven, correct, measured before and after, equivalence proven. 3: measurable improvement,
thinner evidence. 2: claimed improvement, weak evidence. 1: no analysis or incorrect result.

**F. Professional practice (10 %)**
4: one fix per commit with a cause in the message, CI green, PR and postmortem complete and concise.
3: minor gaps. 2: inconsistent. 1: minimal.

## Grade mapping

Weighted mean of the levels: ≥ 3.5 A, 3.0-3.49 B, 2.5-2.99 C, 2.0-2.49 D, below 2 fail. Lab deliverables are
graded on A-D; the performance report on E and B; the capstone on all six.
