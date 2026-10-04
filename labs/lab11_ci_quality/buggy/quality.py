"""Shift report helpers. The CI pipeline for this module is red on all three jobs: lint, types, tests."""
import os
import math
from datetime import datetime, timedelta


def shift_for(timestamp: datetime) -> str:
    """Name of the shift ('night', 'day', 'evening') for a timestamp."""
    hour = timestamp.hour
    if hour < 6:
        return "night"
    elif hour < 14:
        return "day"
    elif hour < 22:
        return "evening"
    else:
        return "night"


def shift_counts(timestamps: list[datetime]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for t in timestamps:
        counts[shift_for(t)] = counts.get(shift_for(t), 0) + 1
    return counts


def hours_between(a: datetime, b: datetime) -> int:
    """Whole hours between two timestamps (always non-negative)."""
    delta = b - a if b > a else a - b
    return delta.total_seconds() / 3600


def format_duration(hours: float) -> str:
    """'2 h 30 min' style formatting for a duration in hours; for example 2.5 hours becomes '2 h 30 min', 0.25 hours becomes '0 h 15 min'."""
    whole = int(hours)
    minutes = round((hours - whole) * 60)
    return f"{whole} h {minutes} min"


def report(timestamps: list[datetime]) -> str:
    counts = shift_counts(timestamps)
    span = hours_between(min(timestamps), max(timestamps)) if timestamps else 0
    lines = [f"{shift}: {n}" for shift, n in sorted(counts.items())]
    lines.append(f"span: {format_duration(span)}")
    return "\n".join(lines)
