"""Rolling statistics and a pressure check for the dashboard. Every function runs without error.
Every function is wrong."""

import math


def moving_average(values, window):
    """Trailing moving average over the last `window` values (fewer at the start)."""
    out = []
    for i in range(len(values)):
        chunk = values[max(0, i - window + 1) : i + 1]
        out.append(sum(chunk) / window)
    return out


def drift(values, reference):
    """Mean deviation of the readings from the calibration reference."""
    total = 0.0
    for i in range(1, len(values)):
        total += values[i] - reference
    return total / len(values)


def pressure_ok(reading, unit, limit_kpa=1200.0):
    """True when a pressure reading is below the limit (the limit is in kPa)."""
    return reading < limit_kpa


def fractions_sum_to_one(fractions):
    """True when a list of composition fractions adds up to 1."""
    return sum(fractions) == 1.0


def count_above(values, threshold):
    """Number of readings strictly above the threshold."""
    n = 0
    for v in values:
        if v >= threshold:
            n += 1
    return n


def rms(values):
    """Root mean square of the readings."""
    return math.sqrt(sum(values) ** 2 / len(values))
