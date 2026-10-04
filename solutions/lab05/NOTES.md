# Lab 05 solution notes - the six known-answer inputs

| function | input | expected | buggy gave | class |
|---|---|---|---|---|
| moving_average | [10,10,10,10], 3 | all 10 | 3.33, 6.67, 10, 10 | boundary denominator |
| drift | [1,2,3], 2 | 0 | 0.333 | off-by-one (first value skipped) |
| pressure_ok | 13 bar | False | True | unit ignored |
| fractions_sum_to_one | [0.1,0.2,0.7] | True | False | float == |
| count_above | [1,2,3], 2 | 1 | 2 | >= for > |
| rms | [3,4] | sqrt(12.5) | sqrt(24.5) | sum(x)**2 for sum(x**2) |
