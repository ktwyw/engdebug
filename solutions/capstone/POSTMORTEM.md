# Postmortem: release candidate 0.2.0-rc1 (three incidents)

**Summary.** Three regressions shipped in one release candidate: a file-encoding change broke ingestion of
files with a byte-order mark (INC-101), a dropped `abs()` made negative drift invisible (INC-102), and a
rewrite of `group_by_sensor` made it quadratic (INC-103). None were caught before the release because the
0.1.0 test suite had no test for a BOM file, no test with a negative drift, and no performance test.

## Timeline

- Fri 16:10 - rc1 cut from the branch "cleanup-ingestion".
- Sat 02:00 - monthly batch job times out (INC-103 raised by the scheduler).
- Sat 08:30 - ops report the March file rejected (INC-101).
- Mon 09:00 - process engineer asks why T102's downward drift never alerted (INC-102).
- Mon 10:00 - on-call reproduces all three with the acceptance tests; fixes landed by 14:00.

## INC-101 - data handling

*Symptom.* `IngestionError: missing columns ['timestamp']; found ['\ufefftimestamp', ...]`.
*Root cause.* `open(path, encoding="utf-8-sig")` was changed to `encoding="utf-8"` ("sig is non-standard").
The BOM is then part of the first header name, so `timestamp` is not found.
*Fix.* Restore `utf-8-sig`. *Regression test.* `test_corrupted_file_is_handled_not_rejected` on the March
file. *Detection gap.* No unit test loaded a file with a BOM, though one was in `datasets/corrupted/`.

## INC-102 - logic

*Symptom.* No drift alert for a sensor 5 degrees below its reference.
*Root cause.* `if abs(d) > max_drift` became `if d > max_drift` in a "simplification" commit; drift is
signed and the alert must fire in both directions.
*Fix.* Restore `abs`. *Regression test.* `test_negative_drift_is_alerted`. *Detection gap.* The only drift
test used a positive drift.

## INC-103 - performance

*Symptom.* The monthly job (51 840 records) runs for minutes; a day takes two seconds instead of 0.1.
*Root cause.* `group_by_sensor` was rewritten to build each sensor's list with a comprehension over all
records, *inside* the loop over records: O(n^2) instead of O(n). `cProfile` on a day shows the
comprehension at 95 % of the time.
*Fix.* One pass with `setdefault`, then sort each group. *Measurement.* day 2.1 s -> 0.09 s; month
> 600 s (timed out) -> 1.9 s. *Regression test.* `test_month_runs_in_under_ten_seconds` (a generous limit:
a performance test should catch a 100x regression, not a 10 % one).

## Prevention

- Keep the corrupted datasets in the integration suite (they were in the repository but not in the tests).
- Every alert rule gets a test in both directions.
- A performance test with a generous bound on the largest realistic input, run in CI.
- Review rule: a commit titled "cleanup" or "simplification" that touches an `encoding=`, an `abs(`, or a
  loop body gets a second reviewer.
