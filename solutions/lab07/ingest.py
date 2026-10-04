"""Ingestion stage (fixed): the contract is a list of row dicts.

Contract: load(path) -> list of {"timestamp": str, "sensor_id": str, "reading": float, "unit": str},
one per data row, in file order. Raises KeyError naming the missing column if the header lacks one.
"""

import csv

REQUIRED = ("timestamp", "sensor_id", "reading", "unit")


def load(path):
    records = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            raise KeyError(f"{path}: missing columns {missing}")
        for row in reader:
            records.append({"timestamp": row["timestamp"], "sensor_id": row["sensor_id"], "reading": float(row["reading"]), "unit": row["unit"]})
    return records


def as_columns(records):
    """The columnar form, derived when (and only when) something needs it."""
    return {key: [rec[key] for rec in records] for key in REQUIRED}
