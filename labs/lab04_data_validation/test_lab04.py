"""Lab 04 check.  Run with:  python -m pytest labs/lab04_data_validation -q"""

import importlib.util
import os
from datetime import datetime
from pathlib import Path

SRC = Path(os.environ.get("ENGDEBUG_LAB_SRC", Path(__file__).parent / "buggy"))
DATA = Path(__file__).resolve().parents[2] / "datasets"
spec = importlib.util.spec_from_file_location("parse", SRC / "parse.py")
parse = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parse)


def test_january_style_file_still_works(tmp_path):
    p = tmp_path / "jan.csv"
    p.write_text("timestamp,sensor_id,reading,unit\n2026-01-05 00:00:00,T101,70.0,degC\n")
    assert parse.parse_file(p)[0]["reading"] == 70.0


def test_march_file_parses_without_crashing():
    recs, problems = parse.parse_file(DATA / "corrupted" / "sensor_day1_corrupted.csv", report_problems=True)
    assert len(recs) >= 1725
    assert len(problems) >= 2 and all(isinstance(row, int) for row, _ in problems)


def test_bom_and_capitalised_header(tmp_path):
    p = tmp_path / "bom.csv"
    p.write_bytes(b"\xef\xbb\xbfTimestamp,Sensor_ID,Reading,Unit\r\n2026-03-02 00:00:00,T101,70.0,degC\r\n")
    assert parse.parse_file(p)[0]["sensor_id"] == "T101"


def test_decimal_comma_and_second_timestamp_format(tmp_path):
    p = tmp_path / "fmt.csv"
    p.write_text('timestamp,sensor_id,reading,unit\n2026-03-02T00:05:00,T101,"70,5",degC\n')
    rec = parse.parse_file(p)[0]
    assert rec["reading"] == 70.5 and rec["timestamp"] == datetime(2026, 3, 2, 0, 5)


def test_placeholders_are_problems_not_zeros(tmp_path):
    p = tmp_path / "na.csv"
    p.write_text("timestamp,sensor_id,reading,unit\n2026-03-02 00:00:00,T101,N/A,degC\n2026-03-02 00:05:00,T101,,degC\n")
    recs, problems = parse.parse_file(p, report_problems=True)
    assert recs == [] and len(problems) == 2


def test_blank_lines_are_skipped(tmp_path):
    p = tmp_path / "blank.csv"
    p.write_text("timestamp,sensor_id,reading,unit\n2026-03-02 00:00:00,T101,70.0,degC\n\n2026-03-02 00:05:00,T101,71.0,degC\n")
    assert len(parse.parse_file(p)) == 2


def test_validate_boundaries_inclusive_and_unknown_unit_rejected():
    t = datetime(2026, 3, 2)
    recs = [{"timestamp": t, "sensor_id": "T", "reading": 0.0, "unit": "bar"}, {"timestamp": t, "sensor_id": "T", "reading": 400.0, "unit": "degC"}, {"timestamp": t, "sensor_id": "T", "reading": 1.0, "unit": "degF"}, {"timestamp": t, "sensor_id": "T", "reading": 9999.0, "unit": "degC"}]
    good = parse.validate(recs)
    assert [r["reading"] for r in good] == [0.0, 400.0]
