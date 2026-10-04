from datetime import datetime, timedelta

import pytest

from engdebug import alerting, models
from engdebug.exceptions import ConfigError


class TestSensor:
    def test_readings_are_per_instance(self):
        a, b = models.Sensor("A", "degC"), models.Sensor("B", "degC")
        a.add(datetime(2026, 3, 2), 1.0)
        assert b.readings == [] and a.latest == 1.0

    def test_add_enforces_time_order(self):
        s = models.Sensor("A", "degC")
        s.add(datetime(2026, 3, 2, 1), 1.0)
        with pytest.raises(ValueError, match="not after"):
            s.add(datetime(2026, 3, 2, 1), 2.0)

    def test_summary(self):
        s = models.Sensor("A", "degC")
        assert s.summary()["n"] == 0 and s.latest is None
        for i in range(3):
            s.add(datetime(2026, 3, 2) + timedelta(minutes=i), float(i))
        assert s.summary()["mean"] == 1.0


class TestEquipment:
    def test_transitions(self):
        e = models.Equipment("pump")
        e.set_status("running")
        e.set_status("fault")
        with pytest.raises(ValueError, match="cannot go from 'fault' to 'running'"):
            e.set_status("running")
        assert e.history == [("stopped", "running"), ("running", "fault")]

    def test_unknown_status(self):
        with pytest.raises(ValueError):
            models.Equipment("pump", status="broken")

    def test_attach_and_lookup(self):
        e = models.Equipment("pump")
        s = models.Sensor("T1", "degC")
        e.attach(s)
        assert e.sensor("T1") is s
        with pytest.raises(ValueError, match="already attached"):
            e.attach(s)
        with pytest.raises(KeyError, match="no sensor 'T9'"):
            e.sensor("T9")
        assert "pump" in repr(e)


class TestAlerting:
    def test_threshold_alerts(self, records):
        recs = records + [dict(records[0], reading=150.0), dict(records[1], reading=0.1)]
        alerts = alerting.threshold_alerts(recs)
        kinds = sorted(a["kind"] for a in alerts)
        assert kinds == ["high", "low"]

    def test_threshold_config_errors(self, records):
        with pytest.raises(ConfigError, match="no thresholds"):
            alerting.threshold_alerts(records, {"bar": {"low": 0, "high": 1}})
        with pytest.raises(ConfigError, match="must be a number"):
            alerting.threshold_alerts(records, {"degC": {"low": "0", "high": "100"}, "bar": {"low": 0, "high": 1}})
        with pytest.raises(ConfigError, match="low .* must be below"):
            alerting.threshold_alerts(records, {"degC": {"low": 100, "high": 0}, "bar": {"low": 0, "high": 1}})

    def test_drift_alerts(self, records):
        from engdebug.ingestion import group_by_sensor

        groups = group_by_sensor(records)
        assert alerting.drift_alerts(groups, {"T101": 70.0}, max_drift=1.0)[0]["kind"] == "drift"
        assert alerting.drift_alerts(groups, {"T101": 72.5}, max_drift=1.0) == []
        assert alerting.drift_alerts(groups, {}, max_drift=1.0) == []

    def test_anomaly_alerts(self):
        t0 = datetime(2026, 3, 2)
        recs = [
            {"timestamp": t0 + timedelta(minutes=i), "sensor_id": "T", "reading": v, "unit": "degC"}
            for i, v in enumerate([10.0, 10.5] * 10 + [40.0])
        ]
        alerts = alerting.anomaly_alerts({"T": recs}, z_limit=4.0)
        assert len(alerts) == 1 and alerts[0]["timestamp"] == recs[-1]["timestamp"]
