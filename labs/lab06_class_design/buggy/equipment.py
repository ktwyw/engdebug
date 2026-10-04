"""Sensor and Equipment classes. Pump 2 keeps showing pump 1's readings, and a pump in 'fault' was
switched straight to 'running' last week."""


class Sensor:
    history = []

    def __init__(self, sensor_id, unit, readings=[]):
        self.sensor_id = sensor_id
        self.unit = unit
        self.readings = readings

    def add(self, timestamp, value):
        self.readings.append((timestamp, value))
        Sensor.history.append(self.sensor_id)

    def latest(self):
        return self.readings[-1][1]

    def mean(self):
        return sum(v for _, v in self.readings) / len(self.readings)


class Equipment:
    def __init__(self, name):
        self.name = name
        self.status = "stopped"
        self.sensors = {}

    def set_status(self, new):
        self.status = new

    def attach(self, sensor):
        self.sensors[sensor.sensor_id] = sensor

    def __eq__(self, other):
        return self.name == other.name
