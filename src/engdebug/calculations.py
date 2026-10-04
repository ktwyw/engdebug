"""Engineering calculations on validated readings.

All functions take plain Python numbers or lists so that they are easy to test; the vectorised versions
in ``optimization``-style labs are compared against these as the reference.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from .exceptions import CalculationError

BAR_PER_KPA = 0.01
KPA_PER_BAR = 100.0


def efficiency(output_kw: float, input_kw: float) -> float:
    """Efficiency = useful output / input, as a fraction in [0, 1]. Raises for non-positive input or output > input."""
    if input_kw <= 0:
        raise CalculationError(f"input power must be positive, got {input_kw}")
    if output_kw < 0:
        raise CalculationError(f"output power cannot be negative, got {output_kw}")
    if output_kw > input_kw * (1 + 1e-9):
        raise CalculationError(f"output {output_kw} exceeds input {input_kw}: check the sensors")
    return min(output_kw / input_kw, 1.0)


def to_kpa(value: float, unit: str) -> float:
    """Convert a pressure to kPa from 'kPa' or 'bar'."""
    if unit == "kPa":
        return value
    if unit == "bar":
        return value * KPA_PER_BAR
    raise CalculationError(f"cannot convert pressure from unit {unit!r}")


def moving_average(values: Sequence[float], window: int) -> list[float]:
    """Trailing moving average: out[i] is the mean of the values in (i - window, i], i.e. of the available
    values when fewer than ``window`` have been seen. Raises ValueError for window < 1."""
    if window < 1:
        raise ValueError(f"window must be >= 1, got {window}")
    out = []
    total = 0.0  # a running sum: add the new value, drop the one that left the window - O(1) per step
    for i, v in enumerate(values):
        total += v
        if i >= window:
            total -= values[i - window]
        out.append(total / min(i + 1, window))  # divide by the number of values actually in the window
    return out


def drift(values: Sequence[float], reference: float) -> float:
    """Mean deviation of the readings from a reference value (the calibration point)."""
    if len(values) == 0:
        raise CalculationError("drift of an empty series is undefined")
    return sum(v - reference for v in values) / len(values)


def mean_and_std(values: Sequence[float]) -> tuple[float, float]:
    """Sample mean and standard deviation (ddof = 1); std is 0 for a single value."""
    n = len(values)
    if n == 0:
        raise CalculationError("mean of an empty series is undefined")
    mean = sum(values) / n
    if n == 1:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in values) / (n - 1)
    return mean, math.sqrt(var)


def anomaly_scores(values: Sequence[float], window: int = 20) -> list[float]:
    """Rolling z-score of each value against the mean and std of the previous ``window`` values
    (0.0 while fewer than two previous values exist or their std is zero)."""
    out = []
    for i in range(len(values)):
        prev = values[max(0, i - window) : i]  # a slice, never a scan of the whole series (lab 09)
        if len(prev) < 2:
            out.append(0.0)  # not enough history to judge
            continue
        m, s = mean_and_std(prev)  # recomputed per window: O(n * w), fine for w = 20; lab 10 shows the O(1) update
        out.append(0.0 if s == 0 else (values[i] - m) / s)
    return out


def isclose(a: float, b: float, rel_tol: float = 1e-9, abs_tol: float = 1e-12) -> bool:
    """Floating-point comparison with tolerances (never compare floats with ==)."""
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def interpolate(x: float, xs: Sequence[float], ys: Sequence[float]) -> float:
    """Linear interpolation of a calibration table; raises for x outside the table."""
    if len(xs) != len(ys) or len(xs) < 2:
        raise CalculationError("calibration table needs at least two points of equal length")
    if x < xs[0] or x > xs[-1]:
        raise CalculationError(f"x = {x} outside the calibration range [{xs[0]}, {xs[-1]}]")
    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]:
            t = (x - xs[i]) / (xs[i + 1] - xs[i]) if xs[i + 1] != xs[i] else 0.0
            return ys[i] + t * (ys[i + 1] - ys[i])
    return ys[-1]
