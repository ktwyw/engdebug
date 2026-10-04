"""Parse the day's readings file into clean records. Works on the file the vendor sent in January.
Fails on the file they sent in March, which "looks the same"."""

import csv
from datetime import datetime


def parse_file(path):
    records = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(
                {
                    "timestamp": datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    "sensor_id": row["sensor_id"],
                    "reading": float(row["reading"]),
                    "unit": row["unit"],
                }
            )
    return records


def validate(records):
    """Return only the records with a plausible reading for their unit."""
    limits = {"degC": (-50, 400), "bar": (0, 50), "kPa": (0, 5000), "kW": (0, 10000), "rpm": (0, 20000)}
    good = []
    for rec in records:
        lo, hi = limits[rec["unit"]]
        if lo < rec["reading"] < hi:
            good.append(rec)
    return good
