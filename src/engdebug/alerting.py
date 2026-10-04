"""Threshold and trend alerts.

An alert is a dict with ``sensor_id``, ``kind`` ('high', 'low', 'drift', 'anomaly'), ``value``, ``limit``
and ``timestamp``. Thresholds are numbers; the comparison must never be done on strings.
"""

from __future__ import annotations

from .calculations import anomaly_scores, drift
from .exceptions import ConfigError

DEFAULT_THRESHOLDS = {
    "degC": {"low": -10.0, "high": 120.0},
    "bar": {"low": 0.5, "high": 12.0},
    "kPa": {"low": 50.0, "high": 1200.0},
    "kW": {"low": 0.0, "high": 900.0},
    "rpm": {"low": 100.0, "high": 3600.0},
    "pct": {"low": 5.0, "high": 95.0},
}


def _limits(unit: str, thresholds: dict | None) -> dict:
    table = thresholds if thresholds is not None else DEFAULT_THRESHOLDS
    if unit not in table:
        raise ConfigError(f"no thresholds configured for unit {unit!r}")
    lim = table[unit]
    for key in ("low", "high"):
        if key not in lim:
            raise ConfigError(f"thresholds for {unit!r} lack {key!r}")
        if not isinstance(lim[key], (int, float)):
            raise ConfigError(f"threshold {key!r} for {unit!r} must be a number, got {lim[key]!r}")
    if lim["low"] >= lim["high"]:
        raise ConfigError(f"thresholds for {unit!r}: low {lim['low']} must be below high {lim['high']}")
    return lim


def threshold_alerts(records: list[dict], thresholds: dict | None = None) -> list[dict]:
    """One alert per record whose reading is outside [low, high] for its unit."""
    alerts = []
    for rec in records:
        lim = _limits(rec["unit"], thresholds)
        if rec["reading"] > lim["high"]:
            alerts.append(
                {
                    "sensor_id": rec["sensor_id"],
                    "kind": "high",
                    "value": rec["reading"],
                    "limit": lim["high"],
                    "timestamp": rec["timestamp"],
                }
            )
        elif rec["reading"] < lim["low"]:
            alerts.append(
                {
                    "sensor_id": rec["sensor_id"],
                    "kind": "low",
                    "value": rec["reading"],
                    "limit": lim["low"],
                    "timestamp": rec["timestamp"],
                }
            )
    return alerts


def drift_alerts(groups: dict[str, list[dict]], references: dict[str, float], max_drift: float) -> list[dict]:
    """One alert per sensor whose mean deviation from its reference exceeds max_drift in absolute value."""
    alerts = []
    for sensor_id, recs in groups.items():
        if sensor_id not in references or not recs:
            continue
        d = drift([r["reading"] for r in recs], references[sensor_id])
        if abs(d) > max_drift:
            alerts.append(
                {
                    "sensor_id": sensor_id,
                    "kind": "drift",
                    "value": d,
                    "limit": max_drift,
                    "timestamp": recs[-1]["timestamp"],
                }
            )
    return alerts


def anomaly_alerts(groups: dict[str, list[dict]], z_limit: float = 4.0, window: int = 20) -> list[dict]:
    """One alert per reading whose rolling z-score exceeds z_limit in absolute value."""
    alerts = []
    for sensor_id, recs in groups.items():
        scores = anomaly_scores([r["reading"] for r in recs], window)
        for rec, z in zip(recs, scores):
            if abs(z) > z_limit:
                alerts.append(
                    {
                        "sensor_id": sensor_id,
                        "kind": "anomaly",
                        "value": z,
                        "limit": z_limit,
                        "timestamp": rec["timestamp"],
                    }
                )
    return alerts
