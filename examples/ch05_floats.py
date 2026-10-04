"""Chapter 5: floating point, boundaries and a unit mix-up - three wrong answers without a traceback.
Run:  python examples/ch05_floats.py"""

import math

print("0.1 + 0.2 == 0.3 ->", 0.1 + 0.2 == 0.3)
print("math.isclose     ->", math.isclose(0.1 + 0.2, 0.3))
print("sum of ten 0.1   ->", repr(sum([0.1] * 10)))


def moving_average_buggy(values, window):
    return [sum(values[max(0, i - window + 1) : i + 1]) / window for i in range(len(values))]


def moving_average(values, window):
    out = []
    for i in range(len(values)):
        chunk = values[max(0, i - window + 1) : i + 1]
        out.append(sum(chunk) / len(chunk))
    return out


print("buggy  average of [10,10,10,10], window 3:", moving_average_buggy([10, 10, 10, 10], 3))
print("fixed  average of [10,10,10,10], window 3:", moving_average([10, 10, 10, 10], 3))

KPA_PER_BAR = 100.0
reading_bar, limit_kpa = 13.0, 1200.0
print("13 bar < 1200 kPa limit, compared raw     ->", reading_bar < limit_kpa, "(wrong: units mixed)")
print("13 bar < 1200 kPa limit, converted to kPa ->", reading_bar * KPA_PER_BAR < limit_kpa)
