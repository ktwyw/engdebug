"""Anomaly detection for a month of readings. Correct, and takes minutes on the large file.
The team's reaction so far: "Python is slow". Measure before you believe that."""

import csv
import math
from datetime import datetime


def load(path):
    records = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            records.append({"timestamp": datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"), "sensor_id": row["sensor_id"], "reading": float(row["reading"]), "unit": row["unit"]})
    return records


def sensor_ids(records):
    ids = []
    for rec in records:
        if rec["sensor_id"] not in ids:
            ids.append(rec["sensor_id"])
    return ids


def readings_for(records, sensor_id):
    return [rec["reading"] for rec in records if rec["sensor_id"] == sensor_id]


def mean(values):
    return sum(values) / len(values)


def std(values):
    m = mean(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))


def anomaly_scores(values, window=20):
    scores = []
    for i in range(len(values)):
        prev = [v for j, v in enumerate(values) if i - window <= j < i]  # "the previous window"
        if len(prev) < 2:
            scores.append(0.0)
            continue
        s = std(prev)
        scores.append(0.0 if s == 0 else (values[i] - mean(prev)) / s)
    return scores


def flagged(records, z_limit=4.0, window=20):
    report = ""
    for sid in sensor_ids(records):
        values = readings_for(records, sid)
        scores = anomaly_scores(values, window)
        for i, z in enumerate(scores):
            if abs(z) > z_limit:
                stamp = [rec for rec in records if rec["sensor_id"] == sid][i]["timestamp"]
                report += f"{sid},{stamp:%Y-%m-%d %H:%M},{z:.2f}\n"
    return report


def run(path):
    return flagged(load(path))


def timed(fn, *args, **kwargs):
    """Run fn and return (result, seconds) measured with time.perf_counter."""
    import time

    t0 = time.perf_counter()
    result = fn(*args, **kwargs)
    return result, time.perf_counter() - t0
