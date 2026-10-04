"""Reading sensor CSV files into records.

A record is a dict with keys ``timestamp`` (datetime), ``sensor_id`` (str), ``reading`` (float) and
``unit`` (str). Files may carry a UTF-8 byte-order mark, Windows line endings, blank lines, and the
occasional unparseable row; the loader reports every problem with the file name and row number.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from .exceptions import IngestionError

REQUIRED_COLUMNS = ("timestamp", "sensor_id", "reading", "unit")
TIMESTAMP_FORMATS = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M")


def parse_timestamp(text: str) -> datetime:
    """Parse the timestamp formats the plant's loggers produce."""
    text = text.strip()
    for fmt in TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    raise ValueError(f"unrecognised timestamp {text!r} (expected one of {TIMESTAMP_FORMATS})")


def parse_reading(text: str) -> float:
    """Parse a numeric reading; accepts a decimal comma, rejects blanks and placeholders."""
    cleaned = text.strip().replace(",", ".")
    if cleaned == "" or cleaned.upper() in {"N/A", "NA", "NAN", "NULL", "-"}:
        raise ValueError(f"missing reading {text!r}")
    return float(cleaned)


def load_readings(path, *, skip_bad_rows: bool = False, bad_rows: list | None = None) -> list[dict]:
    """Load a CSV of sensor readings into a list of records.

    With ``skip_bad_rows=False`` (the default) the first malformed row raises ``IngestionError`` naming the
    file and row. With ``skip_bad_rows=True`` malformed rows are skipped and, if ``bad_rows`` is a list,
    appended to it as ``(row_number, reason)`` so that nothing is silently lost.
    """
    path = Path(path)
    if not path.exists():
        raise IngestionError(path, "file not found")
    records = []
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise IngestionError(path, "file is empty")
        fields = [c.strip().lower() for c in reader.fieldnames]
        missing = [c for c in REQUIRED_COLUMNS if c not in fields]
        if missing:
            raise IngestionError(path, f"missing columns {missing}; found {reader.fieldnames}")
        for row_number, raw in enumerate(reader, start=2):  # row 1 is the header
            row = {k.strip().lower(): (v or "") for k, v in raw.items() if k is not None}
            if not any(v.strip() for v in row.values()):
                continue  # blank line
            try:
                records.append(
                    {
                        "timestamp": parse_timestamp(row["timestamp"]),
                        "sensor_id": row["sensor_id"].strip(),
                        "reading": parse_reading(row["reading"]),
                        "unit": row["unit"].strip(),
                    }
                )
            except (ValueError, KeyError) as exc:
                if not skip_bad_rows:
                    raise IngestionError(path, str(exc), row=row_number) from exc
                if bad_rows is not None:
                    bad_rows.append((row_number, str(exc)))
    return records


def group_by_sensor(records: list[dict]) -> dict[str, list[dict]]:
    """Group records by sensor id, each group sorted by timestamp."""
    groups: dict[str, list[dict]] = {}
    for rec in records:
        sid = rec["sensor_id"]
        groups[sid] = sorted([r for r in records if r["sensor_id"] == sid], key=lambda r: r["timestamp"])
    return groups


def drop_duplicates(records: list[dict]) -> tuple[list[dict], int]:
    """Remove exact duplicate records (same timestamp, sensor and reading), keeping the first; return the
    remaining records and the number dropped. Loggers sometimes write a row twice on reconnect."""
    seen = set()
    out = []
    for rec in records:
        key = (rec["timestamp"], rec["sensor_id"], rec["reading"])
        if key in seen:
            continue
        seen.add(key)
        out.append(rec)
    return out, len(records) - len(out)
