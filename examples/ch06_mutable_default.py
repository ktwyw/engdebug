"""Chapter 6: the mutable default and the shared class attribute, proved with id().
Run:  python examples/ch06_mutable_default.py"""


class BuggySensor:
    history = []  # one list for the whole class

    def __init__(self, sensor_id, readings=[]):  # noqa: B006 - the bug this example demonstrates
        self.sensor_id = sensor_id
        self.readings = readings

    def add(self, value):
        self.readings.append(value)
        self.history.append(self.sensor_id)


class Sensor:
    def __init__(self, sensor_id, readings=None):
        self.sensor_id = sensor_id
        self.readings = list(readings) if readings is not None else []
        self.history = []

    def add(self, value):
        self.readings.append(value)
        self.history.append(self.sensor_id)


for cls in (BuggySensor, Sensor):
    a, b = cls("A"), cls("B")
    a.add(1.0)
    print(
        f"{cls.__name__:<12} same readings object: {a.readings is b.readings!s:<6} B.readings={b.readings} B.history={b.history}"
    )
