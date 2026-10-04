from datetime import datetime, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets"


@pytest.fixture
def data_dir():
    return DATA


@pytest.fixture
def records():
    """Twelve clean records for two sensors."""
    t0 = datetime(2026, 3, 2, 0, 0)
    recs = []
    for i in range(6):
        recs.append(
            {"timestamp": t0 + timedelta(minutes=5 * i), "sensor_id": "T101", "reading": 70.0 + i, "unit": "degC"}
        )
        recs.append(
            {"timestamp": t0 + timedelta(minutes=5 * i), "sensor_id": "P101", "reading": 6.0 + 0.1 * i, "unit": "bar"}
        )
    return recs


@pytest.fixture
def csv_file(tmp_path):
    """Factory: write rows to a temporary CSV and return its path."""

    def make(rows, header="timestamp,sensor_id,reading,unit", name="data.csv", newline="\n", bom=False):
        text = newline.join([header] + rows) + newline
        p = tmp_path / name
        p.write_bytes((b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8"))
        return p

    return make
