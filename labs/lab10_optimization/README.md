# Lab 10 · Optimisation with proof

**Read first.** [Chapter 9 · Performance](../../docs/course/09_performance.md) explains every concept this lab uses. **Habits practised:** the old version is the oracle; prefer the right data structure to the clever trick; write the performance test (see [`docs/habits.md`](../../docs/habits.md)).


**Context.** Lab 09 found where the minutes go. Now make the month run in under two seconds without
changing a single character of the output. "Without changing the output" is the hard part: an
optimisation that silently changes a result is a bug with a speed-up attached.

**Time.** 90 minutes. **Prerequisites.** Lab 09 (the baseline profile).

## What you will learn

- the order of operations for performance work: *correct → measured → optimised → re-measured → still correct*
- the big wins, in the order they usually matter: a better algorithm or data structure (quadratic → linear),
  doing work once instead of in a loop, then constant-factor tricks (`"".join`, set membership), and only
  then vectorisation with NumPy
- running statistics: a moving mean and variance can be updated in O(1) per step instead of recomputed
- how to prove equivalence: a test that compares the new output with the old on real data, plus
  floating-point tolerance where the arithmetic order changed

## Reproduce

```bash
python -m pytest labs/lab10_optimization -q        # correctness passes (fast = slow), speed fails
```

## The work

Edit `buggy/fast.py`. Replace the imported functions one at a time, running the tests after each change:

1. **`anomaly_scores`**: take the window by slicing (`values[max(0, i - window):i]`) instead of scanning the
   whole series - this alone turns 20 s into about a second - and then keep running sums `S = Σx` and `Q = Σx²` over the window; mean = S/w and the sample
   variance = (Q − S²/w)/(w − 1). Update both in O(1) when the window slides. Watch the two traps: the
   variance can come out as −1e-15 for a constant window (clamp to 0 before the square root), and the
   result must still agree with the original to 1e-9 (the test checks).
2. **`flagged`**: group the records by sensor *once* (a dict of lists in one pass), so that both the readings
   and the timestamps are available without rescanning. This removes the second hidden O(n²) and the six
   passes of `readings_for`.
3. **`sensor_ids`**: a set for membership, a list for order - or `dict.fromkeys`.
4. **`report`**: collect lines in a list and `"".join` at the end.
5. If you want to go further, replace the window loop with NumPy (`np.cumsum`) - but measure whether it
   helps at this size; for 8 000 values per sensor the running-sum loop may already be fast enough.

## Prove it

Write `buggy/benchmark.md` with a table: *function, before (s), after (s), speed-up*, for the day and the
month, measured with the `timed` helper from lab 09, and a line per change saying what it did and why it
preserved the output. Rerun `cProfile` on the new version: the top entries should now be `load` and
`strptime` - I/O and parsing, which is where a correct program's time belongs.

## Prevent recurrence

A performance test (`tests/performance/`) with a generous limit - the reference has "a month in under a
second" - catches a regression the day it is merged, not the day the operators complain. Keep the slow
version around as the oracle for the equivalence test.

## Hint ladder

Use one hint at a time, only after an honest attempt.

1. Change one function at a time and rerun the equivalence test after each.
2. The window is `values[max(0, i - window):i]` - a slice, not a scan. Then keep running sums.
3. Group the records by sensor once; `dict.fromkeys` for ordered unique ids; `''.join` for the report.

## Deliverable

`fast.py` (tests green, including the two-second limit), `benchmark.md`, and the new profile listing.
