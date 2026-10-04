"""Lab 03 check.  Run with:  python -m pytest labs/lab03_exceptions -q"""

import importlib.util
import os
from pathlib import Path

import pytest

SRC = Path(os.environ.get("ENGDEBUG_LAB_SRC", Path(__file__).parent / "buggy"))
spec = importlib.util.spec_from_file_location("loader", SRC / "loader.py")
loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loader)


def write(tmp_path, rows, header="timestamp,sensor_id,reading,unit"):
    p = tmp_path / "data.csv"
    p.write_text("\n".join([header] + rows) + "\n")
    return p


def test_custom_exception_hierarchy_exists():
    assert issubclass(loader.LoaderError, Exception)
    assert issubclass(loader.BadRowError, loader.LoaderError)


def test_missing_file_raises_with_path(tmp_path):
    with pytest.raises(loader.LoaderError, match="nope.csv"):
        loader.load(tmp_path / "nope.csv")


def test_bad_row_raises_with_row_number_and_value(tmp_path):
    p = write(tmp_path, ["2026-03-02 00:00:00,T101,70.0,degC", "2026-03-02 00:05:00,T101,N/A,degC"])
    with pytest.raises(loader.BadRowError, match=r"row 3.*N/A"):
        loader.load(p)


def test_bad_row_chains_the_original_error(tmp_path):
    p = write(tmp_path, ["2026-03-02 00:00:00,T101,abc,degC"])
    with pytest.raises(loader.BadRowError) as info:
        loader.load(p)
    assert isinstance(info.value.__cause__, ValueError)


def test_missing_column_raises(tmp_path):
    p = write(tmp_path, ["2026-03-02 00:00:00,T101,70.0"], header="timestamp,sensor_id,value")
    with pytest.raises(loader.LoaderError, match="reading"):
        loader.load(p)


def test_good_file_loads(tmp_path):
    p = write(tmp_path, ["2026-03-02 00:00:00,T101,70.0,degC", "2026-03-02 00:05:00,T101,71.0,degC"])
    assert loader.load(p) == [70.0, 71.0]


def test_mean_of_empty_file_raises_not_zero(tmp_path):
    p = write(tmp_path, [])
    with pytest.raises(loader.LoaderError, match="no readings"):
        loader.mean_reading(p)


def test_nothing_is_printed(tmp_path, capsys):
    with pytest.raises(loader.LoaderError):
        loader.load(tmp_path / "nope.csv")
    assert capsys.readouterr().out == ""
