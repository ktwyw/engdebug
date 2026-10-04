"""Shift report helpers (fixed): lint, types and tests all green."""

from datetime import datetime


def shift_for(timestamp: datetime) -> str:
    """Name of the shift ('night', 'day', 'evening') for a timestamp."""
    hour = timestamp.hour
    if hour < 6:
        return "night"
    if hour < 14:
        return "day"
    if hour < 22:
        return "evening"
    return "night"


def shift_counts(timestamps: list[datetime]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for t in timestamps:
        shift = shift_for(t)
        counts[shift] = counts.get(shift, 0) + 1
    return counts


def hours_between(a: datetime, b: datetime) -> int:
    """Whole hours between two timestamps (always non-negative)."""
    delta = b - a if b > a else a - b
    return int(delta.total_seconds() // 3600)


def format_duration(hours: float) -> str:
    """'2 h 30 min' style formatting for a duration in hours.

    For example 2.5 hours becomes '2 h 30 min' and 0.25 hours becomes '0 h 15 min'.
    """
    whole = int(hours)
    minutes = round((hours - whole) * 60)
    return f"{whole} h {minutes} min"


def report(timestamps: list[datetime]) -> str:
    counts = shift_counts(timestamps)
    span = hours_between(min(timestamps), max(timestamps)) if timestamps else 0
    lines = [f"{shift}: {n}" for shift, n in sorted(counts.items())]
    lines.append(f"span: {format_duration(span)}")
    return "\n".join(lines)
