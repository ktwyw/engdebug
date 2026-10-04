# Chapter 9 · Performance: measuring, profiling and optimising with proof

*For labs 09 and 10. Runnable example: `examples/ch09_profile.py`.*

## Three rules

1. **Measure first.** Programmers' guesses about where time goes are wrong most of the time; a profile
   is right every time. Optimising without measuring is rearranging furniture in the dark.
2. **Correctness is not negotiable.** An optimisation that changes the output is a bug with a speed-up
   attached. Keep the slow version as the oracle and test the new one against it.
3. **Re-measure.** The speed-up is the before/after table. "It feels faster" is not evidence.

## How to think about speed: complexity

For a loop over n items that does constant work per item, time grows in proportion to n: *linear*,
O(n). Double the data, double the time. For a loop over n items that *inside* does another loop over
all n items, time grows with n²: *quadratic*. Double the data, quadruple the time; thirty times the
data, nine hundred times the time.

That ratio is the diagnostic. Time your program on a day of data and on a month (30x). Linear code takes
about 30x longer; lab 09's code takes 700x longer, and the shape of that number tells you there is a
quadratic loop before you have opened the file.

Quadratic loops hide in plain sight:

- `x in some_list` inside a loop over items (each `in` scans the list);
- `some_list.index(v)` inside a loop;
- a comprehension over *all* records inside a loop over records
  (`[r for r in records if r["id"] == rec["id"]]`);
- recomputing a statistic over a window from scratch at every step (O(n·w) - quadratic when w grows
  with n);
- `s += piece` for strings in a loop (each `+=` copies the whole string).

The fixes are the same three ideas every time: **a better data structure** (a set or dict for
membership and lookup: O(1) instead of O(n)), **do the work once** (group the records by id in one pass,
then use the groups), and **update instead of recompute** (a running sum changes by one addition and one
subtraction when the window slides).

## Measuring

**Wall-clock time** of a call:

```python
import time
t0 = time.perf_counter()
result = f(data)
print(f"{time.perf_counter() - t0:.3f} s")
```

`perf_counter` is the right clock (high resolution, monotonic); `time.time()` is for dates.

**Small expressions**, many repetitions: `python -m timeit -s "xs = list(range(10000))" "9999 in xs"`.

**Where the time goes**: `cProfile`.

```bash
python -m cProfile -o run.prof script.py args
python -c "import pstats; pstats.Stats('run.prof').sort_stats('cumulative').print_stats(15)"
python -c "import pstats; pstats.Stats('run.prof').sort_stats('tottime').print_stats(10)"
```

Reading the listing: `ncalls` is how many times the function ran; `tottime` is time spent in the
function's own lines; `cumtime` includes everything it called. Sort by `cumulative` to see where time
*accumulates* (the function and its callees - usually the top of your call tree), then by `tottime` to
see where it is *spent* (the leaf that does the work). The two lists together answer "what is slow" and
"why". A function with `ncalls` of 51 840 that should run six times is the clue.

**Memory**: `tracemalloc.start()`, run, `tracemalloc.get_traced_memory()` gives current and peak bytes;
`take_snapshot().statistics("lineno")` lists the lines that allocated most. A dict per record costs a
few hundred bytes; a month is tens of MB, a year hundreds - the point at which lists of floats or NumPy
arrays stop being premature.

## Optimising, in order of payoff

1. **Fix the complexity.** Quadratic to linear is a factor of n - thousands. Nothing else comes close.
2. **Stop repeating work.** Parse once, group once, convert once. `functools.lru_cache` for a pure
   function called repeatedly with the same arguments.
3. **Running statistics.** For a window of size w, keep S = Σx and Q = Σx²; when the window slides,
   add the new value and subtract the old; mean = S/w, variance = (Q − S²/w)/(w − 1). O(1) per step.
   Clamp the variance at zero (floating-point noise) and test against the two-pass version with a
   tolerance.
4. **Constant factors.** `"".join(parts)` instead of `+=`; a set for membership; local variables inside
   hot loops; avoid attribute lookups in the innermost loop.
5. **Vectorise with NumPy** when the algorithm is right and the data are large: `np.cumsum` for running
   sums, boolean masks for filtering. For a few thousand values the conversion may cost more than it
   saves - measure.
6. **I/O.** Batch writes; read a file once; `strptime` is slow - parse timestamps once and keep the
   `datetime`.

What *not* to do: rewrite in another language before profiling ("Python is slow" was lab 09's team's
conclusion, and the profile showed one list comprehension at 93 % of the time); micro-optimise a loop
that the profile says takes 2 %; change the algorithm and the output at the same time.

## Proving the output is unchanged

- Keep the old version as `slow.py`. The equivalence test is `fast.run(f) == slow.run(f)` on real data.
- Where floating-point order changed, compare with `pytest.approx(..., abs=1e-9)` and say so in the
  report.
- Use `hypothesis` to compare the two on random inputs.
- Run the equivalence test after *every* change, not at the end: when it breaks you want to know which
  change broke it.

## The benchmark report

A table - function, before (s), after (s), speed-up - at two input sizes; one line per change saying
what it did and why the output is unchanged; the new profile's top entries. After a good optimisation
the top of the profile is I/O and parsing: the program's time is where a correct program's time belongs.
A performance test with a generous bound (`a month in under two seconds`) goes into the suite, so the
next regression is caught the day it is merged.

## Habits this chapter starts

- **Time it before you touch it.** Two input sizes; the ratio tells you the complexity.
- **Profile, then fix the top entry.** Not the ugliest line - the slowest.
- **The old version is the oracle.** Equivalence test first, speed-up second.
- **Prefer the right data structure to the clever trick.** A dict instead of a list search is worth a
  thousand micro-optimisations.
- **Write the performance test.** A regression that doubles the runtime should fail CI, not surprise the
  night shift.

Next: [Chapter 10 · Tools and workflow](10_tools_and_workflow.md).
