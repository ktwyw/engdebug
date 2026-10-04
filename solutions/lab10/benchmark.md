# Lab 10 - benchmark (before = slow.py, after = fast.py), measured with lab 09's `timed`

| function | before, day (s) | after, day (s) | before, month (s) | after, month (s) | speed-up (month) |
|---|---|---|---|---|---|
| load | 0.01 | 0.01 | 0.32 | 0.32 | 1 (unchanged: I/O and strptime) |
| flagged (incl. scoring) | 0.02 | 0.003 | 20.1 | 0.12 | ~170 |
| run (total) | 0.03 | 0.015 | 20.4 | 0.45 | ~45 |

Changes, in the order the profile ranked them:

1. `anomaly_scores`: the window is a slice, and the mean and variance are kept as running sums S and Q
   updated in O(1) per step; the variance `(Q - S*mu)/(m-1)` is clamped at 0 (floating-point noise on a
   constant window). Scores agree with the two-pass version to 1e-9 on the test series. This is the whole
   20 s.
2. `flagged`: group the records by sensor once, keep each sensor's records so timestamps come from the
   same list as the readings. Removes the comprehension-per-flag and the six `readings_for` passes.
3. `sensor_ids`: `dict.fromkeys` keeps first-seen order without the O(n*k) list membership.
4. `report`: a list of lines joined once.

After optimising, `cProfile` on the month shows `load` (and inside it `strptime`) as the top entry at
about 70 % of the total: the program's time is now where it should be, in reading the data.
