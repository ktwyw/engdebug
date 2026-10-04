# Lab 09 · Profiling: measure before you optimise

**Context.** `slow.py` finds anomalous readings in a month of data. It is correct. It takes minutes. The
team has concluded that "Python is slow" and is talking about a rewrite. Before anyone rewrites anything,
you will measure where the time goes.

**Time.** 60 minutes. **Prerequisites.** Lab 05.

## What you will learn

- `time.perf_counter` for wall-clock timing and `timeit` for small expressions
- `cProfile` + `pstats` for a function-level profile: calls, total time, cumulative time
- reading a profile: the top of `sort_stats("cumulative")` says where the time *accumulates*, the top of
  `sort_stats("tottime")` says where it is *spent*
- the usual suspects: an O(n²) loop hiding in a comprehension, repeated work in a loop, string
  concatenation, `list.index`/`in` on lists
- the rule: never optimise on a hunch; a profile is evidence

## Reproduce

```bash
# a day first (fast), then the month
python -c "
import sys, time; sys.path.insert(0, 'labs/lab09_profiling/buggy'); import slow
for f in ('datasets/clean/sensor_day1.csv', 'datasets/clean/large_day.csv'):
    t = time.perf_counter(); out = slow.run(f); print(f, len(out.splitlines()), 'flags', round(time.perf_counter() - t, 2), 's')
"
```

Note the ratio: the month has 30 times the data. If the time grew 30-fold the code is linear; if it grew
far more, something is quadratic. (Expect about 0.03 s for the day and 20 s for the month: a ratio near
1000 for 30x the data.)

For memory, the same idea with `tracemalloc`:

```bash
python -c "
import sys, tracemalloc; sys.path.insert(0, 'labs/lab09_profiling/buggy'); import slow
tracemalloc.start(); recs = slow.load('datasets/clean/large_day.csv'); cur, peak = tracemalloc.get_traced_memory()
print(f'{len(recs)} records, {peak / 1e6:.0f} MB peak, {peak / len(recs):.0f} bytes per record')
"
```

A dict per record costs about 400 bytes; a month is tens of MB, a year would be hundreds. That is the
point at which columns (lists of floats, or NumPy arrays) stop being premature optimisation.

## Profile

```bash
python -m cProfile -s cumulative -o labs/lab09_profiling/month.prof -c "import sys; sys.path.insert(0, 'labs/lab09_profiling/buggy'); import slow; slow.run('datasets/clean/large_day.csv')"
python -c "import pstats; pstats.Stats('labs/lab09_profiling/month.prof').sort_stats('cumulative').print_stats(15)"
python -c "import pstats; pstats.Stats('labs/lab09_profiling/month.prof').sort_stats('tottime').print_stats(10)"
```

Read both listings. Three questions for each top entry: how many times was it called? is that number
reasonable? what calls it?

## Diagnose

You should find:

- `anomaly_scores` builds "the previous window" by scanning the *whole* series for every point
  (`[v for j, v in enumerate(values) if i - window <= j < i]`): O(n) per point, O(n²) per sensor - the
  dominant cost, and it looks perfectly innocent;
- it then recomputes `mean(prev)` and `std(prev)` from scratch for every window (O(n·w)), and `std` calls
  `mean` again;
- `flagged` rebuilds the full list of a sensor's records inside the inner loop (`[rec for rec in records
  if ...][i]`), once per flagged point - a second hidden O(n²) that only bites when many points are flagged;
- `readings_for` scans all records once per sensor (six full passes instead of one);
- `sensor_ids` uses `not in` on a growing list; `report += ...` builds a string by concatenation.

Rank them by the profile, not by how ugly they look: the first one dominates by a factor of fifty. That
is the lesson - the loop you would have "optimised" first may not be the one that matters.

## Hint ladder

Use one hint at a time, only after an honest attempt.

1. Time the day and the month with `perf_counter`; divide. Linear code would give about 30.
2. `cProfile` sorted by `tottime`: which single line owns most of the time, and how many times was it called?
3. `[v for j, v in enumerate(values) if ...]` visits every element of `values` for every `i`.

## Deliverable

1. Add `timed(fn, *args, **kwargs) -> (result, seconds)` to `slow.py` (use `perf_counter`).
2. Write `buggy/hotspots.md`: the two profile listings (trimmed to the top 10), the measured times for the
   day and the month, and a ranked list of the hotspots with the line of code responsible for each and
   your estimate of its complexity. Do **not** fix anything yet; lab 10 is the fix, and it must be
   measured against this baseline.
