# Syllabus: Testing, Debugging and Optimising Python for Engineers

Twelve weeks, one lab per week, in a Programming-for-Engineers course after the students can write
functions, loops, lists, dicts and simple classes. Each week: a 45-minute session on the topic, the lab
(60-90 minutes, in pairs), a short deliverable.

| week | topic | lab | deliverable |
|---|---|---|---|
| 1 | Debugging foundations: error classes, reading tracebacks, the seven-step workflow | 01 Traceback triage | the student's own traceback checklist |
| 2 | Testing essentials: unit tests, pytest, normal/boundary/error cases | 02 Unit test rescue | first test file |
| 3 | Exceptions and assertions: try/except/else/finally, custom exceptions, chaining, when to assert | 03 Exception design | exception strategy note |
| 4 | Data validation: input contracts, dirty files, repair vs reject | 04 Dirty data | symptom -> cause table |
| 5 | Logic bugs in engineering calculations: boundaries, units, floats, off-by-one | 05 Logic bugs | known-answer table + a regression test |
| 6 | Class design: mutable defaults, instance vs class state, invariants, equality | 06 Class design | invariants list |
| 7 | Integration: contracts between modules, integration tests, configuration | 07 Integration failure | contract paragraph |
| 8 | Logging and observability: levels, context, diagnosing by logs | 08 Logging | diagnostic playbook |
| 9 | Profiling: perf_counter, timeit, cProfile, reading a profile | 09 Profiling | hotspots.md |
| 10 | Optimisation: algorithms and data structures, running statistics, vectorisation, proof of equivalence | 10 Optimisation | benchmark.md |
| 11 | Industrial workflow: CI, lint, types, pull requests, issue templates; environment and configuration bugs | 11 CI and quality, 13 Environment | green CI + PR description |
| 12-13 | Capstone: incident response on a broken release | 12 Capstone | fixes, tests, benchmark, postmortem, 10-minute presentation |

## Grading (suggested)

Labs 01-11 and 13: 35 %. Mid-course practical (a fresh buggy module, 90 minutes, labs 01-07 skills): 20 %.
Performance report (labs 09-10): 15 %. Capstone: 25 %. Professional practice across the course (commit
quality, PR descriptions, CI hygiene): 5 %. Rubrics in `docs/rubrics.md`.

## Measuring impact

Before week 1 and after week 13, give the same 60-minute practical (three bugs: a crash, a wrong number,
a slow function) and record: time to root cause, first-fix success rate (fix passes the tests on the
first attempt), test quality (rubric C), and a self-rated confidence survey (1-5) on "I can find and fix a
bug in code I did not write". The capstone's regression rate (bugs reintroduced during the fix) is the
course's own metric.

## Self-study

The labs stand alone: a learner working through them in order needs only Python 3.10+, `pytest`, and
this repository. Solutions are in `solutions/`; the honest way to use them is after your own attempt.
