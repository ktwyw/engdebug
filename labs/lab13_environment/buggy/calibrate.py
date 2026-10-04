"""Apply the pressure-sensor calibration table to readings. Works on the author's laptop, from the
author's shell, in the author's virtual environment. Fails everywhere else."""

import yaml  # for the optional settings file

CALIBRATION_FILE = "datasets/clean/calibration.csv"


def load_table(path=CALIBRATION_FILE):
    xs, ys = [], []
    with open(path) as f:
        next(f)
        for line in f:
            a, b = line.split(",")
            xs.append(float(a))
            ys.append(float(b))
    return xs, ys


def load_settings(path="settings.yaml"):
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}


def calibrate(reading_kpa, table=None):
    xs, ys = table if table is not None else load_table()
    for i in range(len(xs) - 1):
        if xs[i] <= reading_kpa <= xs[i + 1]:
            t = (reading_kpa - xs[i]) / (xs[i + 1] - xs[i])
            return ys[i] + t * (ys[i + 1] - ys[i])
    raise ValueError(f"{reading_kpa} outside the calibration range")


def tolerance_from_env():
    """Allowed deviation, from the PRESSURE_TOLERANCE environment variable (kPa)."""
    import os

    return os.environ["PRESSURE_TOLERANCE"]
