"""Rolling statistics and a pressure check (fixed)."""

import math

KPA_PER_BAR = 100.0


def moving_average(values, window):
    """Trailing moving average over the last `window` values (fewer at the start)."""
    out = []
    for i in range(len(values)):
        chunk = values[max(0, i - window + 1) : i + 1]
        out.append(sum(chunk) / len(chunk))  # divide by the number of values actually averaged
    return out


def drift(values, reference):
    """Mean deviation of the readings from the calibration reference."""
    return sum(v - reference for v in values) / len(values)  # every value, not range(1, n)


def pressure_ok(reading, unit, limit_kpa=1200.0):
    """True when a pressure reading is below the limit (the limit is in kPa)."""
    if unit == "kPa":
        kpa = reading
    elif unit == "bar":
        kpa = reading * KPA_PER_BAR
    else:
        raise ValueError(f"cannot convert pressure from {unit!r}")
    return kpa < limit_kpa


def fractions_sum_to_one(fractions):
    """True when a list of composition fractions adds up to 1 (within floating-point tolerance)."""
    return math.isclose(sum(fractions), 1.0, rel_tol=1e-9, abs_tol=1e-12)


def count_above(values, threshold):
    """Number of readings strictly above the threshold."""
    return sum(1 for v in values if v > threshold)


def rms(values):
    """Root mean square of the readings."""
    return math.sqrt(sum(v * v for v in values) / len(values))
