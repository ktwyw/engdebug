import json

import pytest

from engdebug import pipeline, reporting
from engdebug.exceptions import ConfigError, IngestionError, ValidationError


def test_clean_day(data_dir):
    result = pipeline.run(data_dir / "clean" / "sensor_day1.csv")
    assert len(result["summary"]) == 6 and result["skipped"] == [] and result["rejected"] == []
    assert all(row["n"] == 288 for row in result["summary"])


def test_day2_detects_excursion_and_drift(data_dir):
    result = pipeline.run(data_dir / "clean" / "sensor_day2.csv", {"references": {"T101": 72.0}, "max_drift": 1.5})
    kinds = {a["kind"] for a in result["alerts"]}
    assert "high" in kinds and "drift" in kinds
    assert any(a["sensor_id"] == "P101" and a["kind"] == "high" for a in result["alerts"])


def test_corrupted_day_is_handled_with_warnings(data_dir, caplog):
    with caplog.at_level("WARNING", logger="engdebug"):
        result = pipeline.run(data_dir / "corrupted" / "sensor_day1_corrupted.csv")
    assert len(result["skipped"]) == 2 and len(result["rejected"]) == 3 and result["duplicates"] == 1
    assert any("skipped row 19" in m for m in caplog.messages)
    assert not any(
        a["value"] == 9999.0 for a in result["alerts"]
    )  # the stuck 9999 degC is rejected by validation, not alerted


def test_strict_mode_stops_at_first_bad_row(data_dir):
    with pytest.raises(IngestionError, match="row 19"):
        pipeline.run(data_dir / "corrupted" / "sensor_day1_corrupted.csv", {"skip_bad_rows": False})


def test_strict_validation(data_dir):
    with pytest.raises(ValidationError):
        pipeline.run(data_dir / "corrupted" / "sensor_day1_corrupted.csv", {"strict_validation": True})


def test_config_errors():
    with pytest.raises(ConfigError, match="unknown configuration key"):
        pipeline.load_config({"treshold": 1})
    with pytest.raises(ConfigError, match="max_drift"):
        pipeline.load_config({"max_drift": 0})


def test_reports(data_dir, tmp_path):
    result = pipeline.run(data_dir / "clean" / "sensor_day1.csv", report_path=tmp_path / "out" / "report.txt")
    assert (tmp_path / "out" / "report.txt").read_text().startswith("Daily summary")
    doc = json.loads(reporting.json_report(result["summary"], result["alerts"]))
    assert doc["summary"][0]["sensor_id"] == "P101" and isinstance(doc["summary"][0]["first"], str)
