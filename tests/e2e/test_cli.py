import subprocess
import sys


def test_cli_runs_and_prints_report(data_dir):
    proc = subprocess.run(
        [sys.executable, "-m", "engdebug.cli", str(data_dir / "clean" / "sensor_day1.csv")],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0 and "Daily summary" in proc.stdout and "6 sensors" in proc.stderr


def test_cli_reports_errors_with_exit_code(data_dir):
    proc = subprocess.run(
        [sys.executable, "-m", "engdebug.cli", str(data_dir / "corrupted" / "sensor_missing_column.csv")],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 1 and "missing columns" in proc.stderr
