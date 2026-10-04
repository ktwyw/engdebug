# Performance playbook

**Rule 1: measure first.** A profile is evidence; a hunch is not. **Rule 2: correctness is not negotiable.**
An optimisation that changes the output is a bug. **Rule 3: re-measure.** The speed-up is the before/after
table, not the diff.

## Measuring

| tool | use it for | one-liner |
|---|---|---|
| `time.perf_counter()` | wall-clock timing of a call | `t = perf_counter(); f(); print(perf_counter() - t)` |
| `timeit` | small expressions, many repetitions | `python -m timeit -s "import math" "math.sqrt(2)"` |
| `cProfile` + `pstats` | which functions the time goes to | `python -m cProfile -o out.prof script.py`; `pstats.Stats("out.prof").sort_stats("cumulative").print_stats(15)` |
| `tracemalloc` | memory: which lines allocate | `tracemalloc.start(); ...; tracemalloc.take_snapshot().statistics("lineno")[:10]` |
| scaling test | is it linear? quadratic? | time at n and 10n: linear grows 10x, quadratic 100x |

Read `cumulative` to find *where time accumulates* (the function and its callees) and `tottime` to find
*where it is spent* (the function's own lines). The `ncalls` column is often the clue: a function called
50 000 times that should be called 6 times.

## The usual causes, in order of payoff

1. **The wrong complexity.** A lookup in a list inside a loop (O(n) each -> O(n²)); a comprehension over all
   records inside a loop over records; recomputing a statistic over a window instead of updating it.
   Fix the algorithm or the data structure: a set or dict for membership, one grouping pass, running sums.
2. **Repeated work.** The same parse, the same file read, the same conversion done per iteration. Do it
   once; cache with `functools.lru_cache` when the inputs repeat.
3. **Python-level loops over numbers.** When the algorithm is right and the data are large, NumPy's
   vectorised operations (`np.cumsum`, boolean masks) are 10-100x faster per element. Measure: for small
   data the conversion costs more than it saves.
4. **I/O in small pieces.** Row-by-row writes, one query per record: batch them.
5. **String building.** `s += ...` in a loop is quadratic; collect and `"".join`.
6. **The wrong container.** Appending to the front of a list; `deque` for queues; `dict` for lookup.

## Proving equivalence

Keep the slow version as the oracle. Test the new one against it on real data (`fast.run(f) == slow.run(f)`)
and on random data with `hypothesis`. Where floating-point order changed, compare with a tolerance and
say so in the benchmark report.

## Reporting

A table with before/after timings for two input sizes, the speed-up, one line per change saying what it
did and why the output is unchanged, and the new profile's top entries. Lab 10's `benchmark.md` is the
template.
