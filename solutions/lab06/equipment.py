"""Sensor and Equipment classes (fixed): per-instance state and enforced invariants."""

ALLOWED = {
    "running": {"stopped", "fault"},
    "stopped": {"running", "maintenance"},
    "maintenance": {"stopped"},
    "fault": {"maintenance", "stopped"},
}


class Sensor:
    """Invariants: readings are in strictly increasing time order; history lists this sensor's own adds."""

    def __init__(self, sensor_id, unit, readings=None):
        self.sensor_id = sensor_id
        self.unit = unit
        self.readings = list(readings) if readings is not None else []  # never a shared default
        self.history = []  # per instance, not per class

    def add(self, timestamp, value):
        if self.readings and timestamp <= self.readings[-1][0]:
            raise ValueError(f"{self.sensor_id}: {timestamp} is not after the last reading at {self.readings[-1][0]}")
        self.readings.append((timestamp, value))
        self.history.append(self.sensor_id)

    def latest(self):
        return self.readings[-1][1] if self.readings else None  # no reading yet is a normal state

    def mean(self):
        if not self.readings:
            raise ValueError(f"{self.sensor_id}: mean of no readings")  # a caller's mistake
        return sum(v for _, v in self.readings) / len(self.readings)


class Equipment:
    """Invariants: status is one of ALLOWED's keys; transitions follow ALLOWED; sensor ids are unique."""

    def __init__(self, name):
        self.name = name
        self.status = "stopped"
        self.sensors = {}

    def set_status(self, new):
        if new not in ALLOWED:
            raise ValueError(f"unknown status {new!r}")
        if new not in ALLOWED[self.status]:
            raise ValueError(f"{self.name}: cannot go from {self.status!r} to {new!r}")
        self.status = new

    def attach(self, sensor):
        if sensor.sensor_id in self.sensors:
            raise ValueError(f"{self.name}: sensor {sensor.sensor_id!r} already attached")
        self.sensors[sensor.sensor_id] = sensor

    def __eq__(self, other):
        if not isinstance(other, Equipment):
            return NotImplemented
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
