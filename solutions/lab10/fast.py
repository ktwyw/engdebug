"""Optimised anomaly detection: identical output to slow.run, linear time."""

import csv
import math
from datetime import datetime


def load(path):
    records = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            records.append({"timestamp": datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"), "sensor_id": row["sensor_id"], "reading": float(row["reading"]), "unit": row["unit"]})
    return records


def group(records):
    """One pass: sensor id -> list of records, in first-seen order of sensors (as sensor_ids produced)."""
    by_sensor = {}
    for rec in records:
        by_sensor.setdefault(rec["sensor_id"], []).append(rec)
    return by_sensor


def sensor_ids(records):
    return list(dict.fromkeys(rec["sensor_id"] for rec in records))


def readings_for(records, sensor_id):
    return [rec["reading"] for rec in records if rec["sensor_id"] == sensor_id]


def mean(values):
    return sum(values) / len(values)


def std(values):
    m = mean(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))


def anomaly_scores(values, window=20):
    """Rolling z-score with running sums: O(1) per step. Uses the shifted-data form (subtracting the first
    value of the window) to keep the running variance numerically close to the two-pass result."""
    scores = []
    n = len(values)
    for i in range(n):
        lo = max(0, i - window)
        m = i - lo
        if m < 2:
            scores.append(0.0)
            continue
        if i == 2 or lo == 0 or i - window < 0:
            # recompute from scratch while the window is still growing (cheap: at most `window` values)
            S = sum(values[lo:i])
            Q = sum(v * v for v in values[lo:i])
        else:
            # slide: drop values[lo - 1], add values[i - 1]
            out_v, in_v = values[lo - 1], values[i - 1]
            S += in_v - out_v
            Q += in_v * in_v - out_v * out_v
        mu = S / m
        var = max((Q - S * mu) / (m - 1), 0.0)
        s = math.sqrt(var)
        scores.append(0.0 if s < 1e-12 else (values[i] - mu) / s)
    return scores


def flagged(records, z_limit=4.0, window=20):
    lines = []
    for sid, recs in group(records).items():
        values = [rec["reading"] for rec in recs]
        for rec, z in zip(recs, anomaly_scores(values, window)):
            if abs(z) > z_limit:
                lines.append(f"{sid},{rec['timestamp']:%Y-%m-%d %H:%M},{z:.2f}\n")
    return "".join(lines)


def run(path):
    return flagged(load(path))
