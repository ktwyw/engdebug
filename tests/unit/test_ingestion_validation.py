from datetime import datetime

import pytest

from engdebug import ingestion, validation
from engdebug.exceptions import IngestionError, ValidationError


class TestParsing:
    @pytest.mark.parametrize("text", ["2026-03-02 10:05:00", "2026-03-02T10:05:00", " 2026-03-02 10:05 "])
    def test_timestamp_formats(self, text):
        assert ingestion.parse_timestamp(text) == datetime(2026, 3, 2, 10, 5)

    def test_bad_timestamp(self):
        with pytest.raises(ValueError, match="unrecognised timestamp"):
            ingestion.parse_timestamp("02/03/2026")

    @pytest.mark.parametrize("text, value", [("6.25", 6.25), (" 6,25 ", 6.25), ("-3", -3.0), ("1e3", 1000.0)])
    def test_readings(self, text, value):
        assert ingestion.parse_reading(text) == value

    @pytest.mark.parametrize("text", ["", "N/A", "nan", "-", "  "])
    def test_missing_readings(self, text):
        with pytest.raises(ValueError, match="missing reading"):
            ingestion.parse_reading(text)


class TestLoading:
    def test_clean_file(self, csv_file):
        p = csv_file(["2026-03-02 00:00:00,T101,70.0,degC", "2026-03-02 00:05:00,T101,70.5,degC"])
        recs = ingestion.load_readings(p)
        assert len(recs) == 2 and recs[1]["reading"] == 70.5 and recs[0]["unit"] == "degC"

    def test_bom_crlf_blank_lines_and_case(self, csv_file):
        p = csv_file(
            ["2026-03-02 00:00:00,T101,70.0,degC", "", "2026-03-02 00:05:00,T101,70.5,degC"],
            header="Timestamp,Sensor_ID,Reading,Unit",
            newline="\r\n",
            bom=True,
        )
        assert len(ingestion.load_readings(p)) == 2

    def test_missing_file(self, tmp_path):
        with pytest.raises(IngestionError, match="file not found"):
            ingestion.load_readings(tmp_path / "nope.csv")

    def test_missing_column(self, csv_file):
        p = csv_file(["2026-03-02 00:00:00,T101,70.0"], header="timestamp,sensor_id,reading")
        with pytest.raises(IngestionError, match=r"missing columns \['unit'\]"):
            ingestion.load_readings(p)

    def test_empty_file(self, tmp_path):
        p = tmp_path / "e.csv"
        p.write_text("")
        with pytest.raises(IngestionError, match="empty"):
            ingestion.load_readings(p)

    def test_bad_row_reports_row_number(self, csv_file):
        p = csv_file(["2026-03-02 00:00:00,T101,70.0,degC", "2026-03-02 00:05:00,T101,N/A,degC"])
        with pytest.raises(IngestionError, match="row 3") as info:
            ingestion.load_readings(p)
        assert info.value.row == 3

    def test_skip_bad_rows_records_them(self, csv_file):
        p = csv_file(["2026-03-02 00:00:00,T101,70.0,degC", "2026-03-02 00:05:00,T101,N/A,degC", "bad,row"])
        bad = []
        recs = ingestion.load_readings(p, skip_bad_rows=True, bad_rows=bad)
        assert len(recs) == 1 and [r for r, _ in bad] == [3, 4]

    def test_group_and_dedupe(self, records):
        dup = records + [records[0]]
        deduped, n = ingestion.drop_duplicates(dup)
        assert n == 1 and len(deduped) == 12
        groups = ingestion.group_by_sensor(deduped)
        assert sorted(groups) == ["P101", "T101"] and all(
            a["timestamp"] < b["timestamp"] for a, b in zip(groups["T101"], groups["T101"][1:])
        )


class TestValidation:
    def test_good_record_passes(self, records):
        assert validation.validate_record(records[0]) is records[0]

    def test_missing_field(self):
        with pytest.raises(ValidationError, match="missing field") as info:
            validation.validate_record({"timestamp": datetime(2026, 3, 2), "sensor_id": "T1", "reading": 1.0})
        assert info.value.field == "unit"

    def test_wrong_type(self, records):
        rec = dict(records[0], reading="70")
        with pytest.raises(ValidationError, match="expected float, got str"):
            validation.validate_record(rec)

    def test_unknown_unit(self, records):
        with pytest.raises(ValidationError, match="unknown unit"):
            validation.validate_record(dict(records[0], unit="degF"))

    @pytest.mark.parametrize("value", [-60.0, 401.0])
    def test_out_of_range(self, records, value):
        with pytest.raises(ValidationError, match="plausible range"):
            validation.validate_record(dict(records[0], reading=value))

    @pytest.mark.parametrize("value", [-50.0, 400.0, 0.0])
    def test_boundaries_inclusive(self, records, value):
        validation.validate_record(dict(records[0], reading=value))

    def test_validate_all_non_strict(self, records):
        recs = records + [dict(records[0], unit="degF")]
        good, rejected = validation.validate_all(recs, strict=False)
        assert len(good) == 12 and rejected[0][0] == 12

    def test_monotonic(self, records):
        validation.check_monotonic_timestamps(ingestion.group_by_sensor(records)["T101"])
        with pytest.raises(ValidationError, match="strictly increasing"):
            validation.check_monotonic_timestamps([records[0], records[0]])
