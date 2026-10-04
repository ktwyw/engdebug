"""Schema, type and range checks on records.

Validation runs after ingestion and before any calculation: a record that passes is guaranteed to have
the right keys, types and plausible values, so the calculations need no defensive code of their own.
"""

from __future__ import annotations

from datetime import datetime

from .exceptions import ValidationError

SCHEMA = {"timestamp": datetime, "sensor_id": str, "reading": float, "unit": str}

# plausible physical ranges per unit; readings outside are rejected (a stuck or miswired sensor)
RANGES = {
    "degC": (-50.0, 400.0),
    "bar": (0.0, 50.0),
    "kPa": (0.0, 5000.0),
    "kW": (0.0, 10000.0),
    "rpm": (0.0, 20000.0),
    "pct": (0.0, 100.0),
}


def validate_record(rec: dict, row: int | None = None) -> dict:
    """Return the record if it satisfies the schema and ranges; raise ValidationError with context otherwise."""
    for key, typ in SCHEMA.items():
        if key not in rec:
            raise ValidationError("missing field", field=key, row=row)
        if not isinstance(rec[key], typ):
            raise ValidationError(f"expected {typ.__name__}, got {type(rec[key]).__name__}", field=key, row=row, value=rec[key])
    if rec["sensor_id"] == "":
        raise ValidationError("empty sensor id", field="sensor_id", row=row)
    unit = rec["unit"]
    if unit not in RANGES:
        raise ValidationError(f"unknown unit (known: {sorted(RANGES)})", field="unit", row=row, value=unit)
    lo, hi = RANGES[unit]
    if not (lo <= rec["reading"] <= hi):
        raise ValidationError(f"reading outside the plausible range [{lo}, {hi}] for {unit}", field="reading", row=row, value=rec["reading"])
    return rec


def validate_all(records: list[dict], *, strict: bool = True) -> tuple[list[dict], list[tuple[int, str]]]:
    """Validate every record. strict=True raises on the first problem; strict=False returns (good, rejected)."""
    good, rejected = [], []
    for i, rec in enumerate(records):
        try:
            good.append(validate_record(rec, row=i))
        except ValidationError as exc:
            if strict:
                raise
            rejected.append((i, str(exc)))
    return good, rejected


def check_monotonic_timestamps(records: list[dict]) -> None:
    """Records of one sensor must be in increasing time order with no duplicates."""
    for prev, cur in zip(records, records[1:]):
        if cur["timestamp"] <= prev["timestamp"]:
            raise ValidationError("timestamps not strictly increasing", field="timestamp", value=cur["timestamp"])
