"""Apply the pressure-sensor calibration table (fixed): no undeclared dependency, no cwd-relative path,
environment variables read once with a default and a conversion."""

import json
import os
from pathlib import Path

CALIBRATION_FILE = Path(__file__).resolve().parents[2] / "datasets" / "clean" / "calibration.csv"


def load_table(path=CALIBRATION_FILE):
    xs, ys = [], []
    with open(path, encoding="utf-8") as f:
        next(f)
        for line in f:
            a, b = line.split(",")
            xs.append(float(a))
            ys.append(float(b))
    return xs, ys


def load_settings(path="settings.json"):
    """Optional settings file; JSON needs no third-party package."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def calibrate(reading_kpa, table=None):
    xs, ys = table if table is not None else load_table()
    for i in range(len(xs) - 1):
        if xs[i] <= reading_kpa <= xs[i + 1]:
            t = (reading_kpa - xs[i]) / (xs[i + 1] - xs[i])
            return ys[i] + t * (ys[i + 1] - ys[i])
    raise ValueError(f"{reading_kpa} outside the calibration range [{xs[0]}, {xs[-1]}]")


def tolerance_from_env(default=5.0):
    """Allowed deviation in kPa from PRESSURE_TOLERANCE; a default when unset, a clear error when not a number."""
    raw = os.environ.get("PRESSURE_TOLERANCE")
    if raw is None:
        return float(default)
    try:
        return float(raw)
    except ValueError:
        raise ValueError(f"PRESSURE_TOLERANCE must be a number, got {raw!r}") from None
