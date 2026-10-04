"""Performance tests: assert that the reference implementations scale as intended."""

import time

import pytest

from engdebug import calculations as calc


@pytest.mark.slow
def test_moving_average_is_linear_time():
    small = list(range(20_000))
    big = list(range(200_000))
    t0 = time.perf_counter()
    calc.moving_average(small, 50)
    t_small = time.perf_counter() - t0
    t0 = time.perf_counter()
    calc.moving_average(big, 50)
    t_big = time.perf_counter() - t0
    assert t_big < 25 * max(t_small, 1e-3)  # ten times the data should not cost more than ~25x (allowing noise)


@pytest.mark.slow
def test_anomaly_scores_under_a_second_for_a_month(data_dir):
    from engdebug import ingestion

    recs = ingestion.load_readings(data_dir / "clean" / "large_day.csv")
    vals = [r["reading"] for r in recs if r["sensor_id"] == "T101"]
    t0 = time.perf_counter()
    calc.anomaly_scores(vals, 20)
    assert time.perf_counter() - t0 < 1.0
