"""Lab 09 check.  Run with:  python -m pytest labs/lab09_profiling -q
The deliverable of this lab is a profile report; the code change is the subject of lab 10. These checks
only require that you have instrumented the module: a timing function and a profile-driven list of
hotspots recorded in hotspots.md."""

import os
from pathlib import Path

HERE = Path(__file__).parent
SRC = Path(os.environ.get("ENGDEBUG_LAB_SRC", HERE / "buggy"))


def test_hotspots_report_exists_and_names_the_top_functions():
    report = SRC / "hotspots.md"
    assert report.exists(), "write hotspots.md next to slow.py with the profile's top entries"
    text = report.read_text().lower()
    assert "cprofile" in text or "profile" in text
    assert "flagged" in text and ("readings_for" in text or "anomaly_scores" in text or "std" in text)
    assert "seconds" in text or " s " in text or "ms" in text, "report the measured time"


def test_timing_helper_exists():
    import importlib.util

    spec = importlib.util.spec_from_file_location("slow", SRC / "slow.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "timed"), "add a timed(fn, *args) helper that returns (result, seconds) using time.perf_counter"
    result, seconds = mod.timed(mod.mean, [1.0, 2.0, 3.0])
    assert result == 2.0 and seconds >= 0
