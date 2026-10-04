"""Ingestion stage, rewritten last sprint to return columns instead of rows ("faster for pandas later")."""

import csv


def load(path):
    columns = {"timestamp": [], "sensor_id": [], "reading": [], "unit": []}
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            for key in columns:
                columns[key].append(row[key])
    columns["reading"] = [float(v) for v in columns["reading"]]
    return columns
