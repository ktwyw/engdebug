"""Every bug fixed in a lab gets a regression test here, named after the lab, so that it stays fixed."""

from datetime import datetime

import pytest

from engdebug import calculations as calc
from engdebug import ingestion, models
from engdebug.exceptions import CalculationError


def test_lab02_efficiency_direction_and_guard():
    # Regression: the formula was inverted (input/output) and divided by zero on a stopped machine.
    assert calc.efficiency(50.0, 100.0) == 0.5
    with pytest.raises(CalculationError):
        calc.efficiency(0.0, 0.0)


def test_lab05_moving_average_boundary_denominator():
    # Regression: the first window-1 values were divided by the full window, biasing them towards zero.
    assert calc.moving_average([10.0, 10.0, 10.0], 3) == [10.0, 10.0, 10.0]


def test_lab05_pressure_units_are_converted_not_compared_raw():
    # Regression: a 6-bar reading was compared with a 600-kPa limit without conversion.
    assert calc.to_kpa(6.0, "bar") == 600.0


def test_lab06_sensor_readings_not_shared_between_instances():
    a, b = models.Sensor("A", "degC"), models.Sensor("B", "degC")
    a.add(datetime(2026, 3, 2), 1.0)
    assert b.readings == []


def test_lab04_decimal_comma_and_placeholders():
    assert ingestion.parse_reading("6,25") == 6.25
    with pytest.raises(ValueError):
        ingestion.parse_reading("N/A")


def test_lab04_bom_header_is_recognised(csv_file):
    p = csv_file(["2026-03-02 00:00:00,T101,70.0,degC"], bom=True)
    assert ingestion.load_readings(p)[0]["sensor_id"] == "T101"


def test_lab07_config_keys_are_validated_with_the_available_keys_named():
    from engdebug import pipeline
    from engdebug.exceptions import ConfigError

    with pytest.raises(ConfigError, match="known:"):
        pipeline.load_config({"threshold": {}})


def test_lab08_unknown_unit_is_a_config_error_not_a_silent_default(records):
    from engdebug import alerting
    from engdebug.exceptions import ConfigError

    with pytest.raises(ConfigError, match="psi"):
        alerting.threshold_alerts([dict(records[0], unit="psi")], {"psi_missing": {}})


def test_lab09_lab10_anomaly_scores_are_linear_in_the_window_not_the_series():
    import time

    small = [float(i % 7) for i in range(2_000)]
    big = [float(i % 7) for i in range(20_000)]
    t0 = time.perf_counter()
    calc.anomaly_scores(small, 20)
    t_small = time.perf_counter() - t0
    t0 = time.perf_counter()
    calc.anomaly_scores(big, 20)
    t_big = time.perf_counter() - t0
    assert t_big < 30 * max(t_small, 1e-3)


def test_lab11_type_annotations_match_behaviour():
    # Regression for the capstone/lab 11 class of bug: a float where the contract says int.
    import inspect

    from engdebug import reporting

    rows = reporting.summarise(
        {"T": [{"timestamp": datetime(2026, 3, 2), "sensor_id": "T", "reading": 1.0, "unit": "degC"}]}
    )
    assert isinstance(rows[0]["n"], int) and inspect.signature(calc.moving_average).return_annotation == "list[float]"


def test_lab13_cli_takes_the_path_as_an_argument_not_from_cwd(tmp_path, data_dir):
    import subprocess
    import sys

    proc = subprocess.run(
        [sys.executable, "-m", "engdebug.cli", str(data_dir / "clean" / "sensor_day1.csv")],
        capture_output=True,
        text=True,
        cwd=tmp_path,
        timeout=60,
    )
    assert proc.returncode == 0


def test_capstone_negative_drift_alerts():
    from engdebug import alerting

    recs = [{"timestamp": datetime(2026, 3, 2), "sensor_id": "T", "reading": 60.0, "unit": "degC"}] * 3
    assert alerting.drift_alerts({"T": recs}, {"T": 65.0}, max_drift=2.0)[0]["value"] == pytest.approx(-5.0)


def test_lab14_units_equations_and_ranges():
    from engdebug import engineering as eng

    assert eng.ideal_gas_volume_m3(1.0, 273.15, 101325.0) == pytest.approx(0.022414, rel=1e-4)  # kelvin, not Celsius
    assert eng.pump_power_w(1.0, 10.0, 1000.0, 1.0) == pytest.approx(98066.5)  # g present, efficiency a fraction
    assert eng.friction_factor(1000.0) == pytest.approx(0.064)  # laminar: 64/Re, never Blasius
    with pytest.raises(CalculationError):
        eng.interpolate_table(11.0, [0.0, 10.0], [0.0, 1.0])  # no silent extrapolation
