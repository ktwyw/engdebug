# Lab 09 - profile of slow.run on the month file (recorded while preparing the solution)

Measured with `timed`: day file 0.03 seconds, month file 20 seconds. The ratio (about 700 for 30x the data) says the
code is quadratic somewhere.

`cProfile`, sorted by cumulative time (top entries, trimmed):

```
   ncalls  tottime  cumtime  filename:lineno(function)
        1    0.000   20.4    slow.py:run
        1    0.001   20.1    slow.py:flagged
        6    0.05    19.6    slow.py:anomaly_scores
    51840   18.9    18.9    slow.py:<listcomp>   ([v for j, v in enumerate(values) if i - window <= j < i])
    51834    0.2     0.6    slow.py:std
   103668    0.3     0.3    slow.py:mean
       49    0.3     0.3    slow.py:<listcomp>   (the records-by-sensor rebuild per flagged point in flagged)
        6    0.05    0.05   slow.py:readings_for
        1    0.3     0.3    slow.py:load   (strptime dominates inside it)
```

Sorted by `tottime` the first list comprehension is 93 % of the total on its own.

Ranked hotspots:

1. `anomaly_scores`, "the previous window" built by scanning the whole series for every point: O(n) per
   point, O(n^2) per sensor. 51 840 calls, 19 s.
2. `anomaly_scores` -> `std` -> `mean`: each window recomputed from scratch, mean computed twice: O(n*w).
3. `flagged`: the list of a sensor's records rebuilt once per flagged point (49 times here; would be
   O(n^2) on a noisy month).
4. `readings_for`: one full pass per sensor (6 passes).
5. `sensor_ids`: `not in` on a list; `report += ...`: quadratic string building (small here).

Only 1 matters at this size; 2 is the next factor of ten; 3-5 are hygiene. Lab 10 fixes them in that
order and measures.
