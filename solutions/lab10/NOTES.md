# Lab 10 solution notes

`fast.py` replaces the functions in the order the profile ranked them and `benchmark.md` records the
before/after numbers. Two details worth the student's attention:

- The running-variance update `(Q - S*mu)/(m - 1)` can produce a tiny negative number for a constant
  window because of floating-point cancellation; it is clamped at zero before the square root. Without
  the clamp `math.sqrt` raises `ValueError: math domain error` on the first flat stretch of data - an
  optimisation that introduced a crash.
- The equivalence test compares the z-scores with `abs=1e-9`, not `==`: the arithmetic order changed,
  so the last digits may differ. The report says so. That is the honest form of "the output is
  unchanged".
