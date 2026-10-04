"""Sensor and Equipment classes with explicit invariants.

The classes hold state (readings, status) and enforce the rules that make the rest of the pipeline
simple: a sensor's readings are always in time order, a piece of equipment knows which sensors it owns,
and status changes follow the allowed transitions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from .calculations import mean_and_std

ALLOWED_TRANSITIONS = {
    "running": {"stopped", "fault"},
    "stopped": {"running", "maintenance"},
    "maintenance": {"stopped"},
    "fault": {"maintenance", "stopped"},
}


@dataclass
class Sensor:
    """A sensor and its readings. ``readings`` is created fresh per instance (never a shared default)."""

    sensor_id: str
    unit: str
    readings: list[tuple[datetime, float]] = field(default_factory=list)

    def add(self, timestamp: datetime, value: float) -> None:
        if self.readings and timestamp <= self.readings[-1][0]:
            raise ValueError(f"{self.sensor_id}: reading at {timestamp} is not after the last one at {self.readings[-1][0]}")
        self.readings.append((timestamp, value))

    @property
    def values(self) -> list[float]:
        return [v for _, v in self.readings]

    @property
    def latest(self) -> float | None:
        return self.readings[-1][1] if self.readings else None

    def summary(self) -> dict:
        if not self.readings:
            return {"sensor_id": self.sensor_id, "n": 0, "mean": None, "std": None}
        m, s = mean_and_std(self.values)
        return {"sensor_id": self.sensor_id, "n": len(self.readings), "mean": m, "std": s}


class Equipment:
    """A piece of equipment that owns sensors and has a status with allowed transitions."""

    def __init__(self, name: str, status: str = "stopped"):
        if status not in ALLOWED_TRANSITIONS:
            raise ValueError(f"unknown status {status!r}")
        self.name = name
        self._status = status
        self.sensors: dict[str, Sensor] = {}
        self.history: list[tuple[str, str]] = []

    @property
    def status(self) -> str:
        return self._status

    def set_status(self, new: str) -> None:
        if new not in ALLOWED_TRANSITIONS:
            raise ValueError(f"unknown status {new!r}")
        if new not in ALLOWED_TRANSITIONS[self._status]:
            raise ValueError(f"{self.name}: cannot go from {self._status!r} to {new!r}")
        self.history.append((self._status, new))
        self._status = new

    def attach(self, sensor: Sensor) -> None:
        if sensor.sensor_id in self.sensors:
            raise ValueError(f"{self.name}: sensor {sensor.sensor_id!r} already attached")
        self.sensors[sensor.sensor_id] = sensor

    def sensor(self, sensor_id: str) -> Sensor:
        try:
            return self.sensors[sensor_id]
        except KeyError:
            raise KeyError(f"{self.name}: no sensor {sensor_id!r}; attached: {sorted(self.sensors)}") from None

    def __repr__(self) -> str:
        return f"Equipment({self.name!r}, status={self._status!r}, sensors={sorted(self.sensors)})"
