"""Parse the day's readings file into clean records (fixed)."""

import csv
from datetime import datetime

REQUIRED = ("timestamp", "sensor_id", "reading", "unit")
TIMESTAMP_FORMATS = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M")
PLACEHOLDERS = {"", "N/A", "NA", "NAN", "NULL", "-"}
LIMITS = {"degC": (-50.0, 400.0), "bar": (0.0, 50.0), "kPa": (0.0, 5000.0), "kW": (0.0, 10000.0), "rpm": (0.0, 20000.0)}


def parse_timestamp(text):
    text = text.strip()
    for fmt in TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError(f"unrecognised timestamp {text!r}")


def parse_reading(text):
    cleaned = text.strip().replace(",", ".")
    if cleaned.upper() in PLACEHOLDERS:
        raise ValueError(f"missing reading {text!r}")
    return float(cleaned)


def parse_file(path, report_problems=False):
    records, problems = [], []
    with open(path, encoding="utf-8-sig", newline="") as f:  # utf-8-sig strips the BOM; newline='' handles CRLF
        reader = csv.DictReader(f)
        fields = [c.strip().lower() for c in (reader.fieldnames or [])]
        missing = [c for c in REQUIRED if c not in fields]
        if missing:
            raise ValueError(f"{path}: missing columns {missing}")
        for row_number, raw in enumerate(reader, start=2):
            row = {k.strip().lower(): (v or "") for k, v in raw.items() if k is not None}
            if not any(v.strip() for v in row.values()):
                continue  # blank line
            try:
                records.append({"timestamp": parse_timestamp(row["timestamp"]), "sensor_id": row["sensor_id"].strip(), "reading": parse_reading(row["reading"]), "unit": row["unit"].strip()})
            except (ValueError, KeyError) as exc:
                if not report_problems:
                    raise ValueError(f"{path}, row {row_number}: {exc}") from exc
                problems.append((row_number, str(exc)))
    return (records, problems) if report_problems else records


def validate(records):
    """Return only the records with a plausible reading for their unit (inclusive bounds; unknown units rejected)."""
    good = []
    for rec in records:
        limits = LIMITS.get(rec["unit"])
        if limits is None:
            continue
        lo, hi = limits
        if lo <= rec["reading"] <= hi:
            good.append(rec)
    return good
