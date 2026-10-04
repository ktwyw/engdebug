"""Daily monitor: threshold and drift alerts. On some days it reports nothing when it should; the
operators call it "intermittent". There is nothing intermittent about it."""

import csv
from datetime import datetime

LIMITS = {"degc": 120.0, "bar": 12.0, "kpa": 1200.0, "kw": 900.0, "rpm": 3600.0}
REFERENCES = {"T101": 72.0, "P101": 6.2, "W101": 340.0, "T102": 65.0, "P102": 610.0}


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return [{"timestamp": datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S"), "sensor_id": r["sensor_id"], "reading": float(r["reading"]), "unit": r["unit"]} for r in csv.DictReader(f)]


def threshold_alerts(records):
    out = []
    for rec in records:
        limit = LIMITS.get(rec["unit"], float("inf"))
        if rec["reading"] > limit:
            out.append((rec["sensor_id"], "high", rec["reading"]))
    return out


def drift_alerts(records, max_drift=1.5):
    out = []
    by_sensor = {}
    for rec in records:
        by_sensor.setdefault(rec["sensor_id"], []).append(rec["reading"])
    for sid, values in by_sensor.items():
        try:
            d = sum(values) / len(values) - REFERENCES[sid]
            if abs(d) > max_drift:
                out.append((sid, "drift", d))
        except Exception:
            pass
    return out


def run(path):
    records = load(path)
    return threshold_alerts(records) + drift_alerts(records)
