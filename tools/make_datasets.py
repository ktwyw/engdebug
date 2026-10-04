"""Write the clean and corrupted datasets into datasets/ (seed 2026). Run: python tools/make_datasets.py

datasets/clean/sensor_day1.csv        one day of readings from six sensors on two pumps (5-minute cadence)
datasets/clean/sensor_day2.csv        the next day, with a slow temperature drift and one pressure excursion
datasets/corrupted/sensor_day1_corrupted.csv   day 1 with: a UTF-8 BOM, Windows line endings, a renamed
                                      column ('Reading'), blank lines, 'N/A' and empty readings, a decimal
                                      comma, a timestamp in a second format, a duplicated row, a reading of
                                      9999 on a temperature sensor, and an unknown unit
datasets/corrupted/sensor_missing_column.csv   the 'unit' column is absent
datasets/corrupted/sensor_empty.csv            header only
datasets/clean/calibration.csv        a pressure-sensor calibration table (kPa reading vs reference)
datasets/clean/large_day.csv          thirty days of readings (profiling and optimisation labs)
"""

from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1] / "datasets"
(ROOT / "clean").mkdir(parents=True, exist_ok=True)
(ROOT / "corrupted").mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(2026)

SENSORS = [
    ("T101", "degC", 72.0, 1.5),
    ("P101", "bar", 6.2, 0.15),
    ("W101", "kW", 340.0, 12.0),
    ("T102", "degC", 65.0, 1.2),
    ("P102", "kPa", 610.0, 15.0),
    ("S102", "rpm", 2950.0, 20.0),
]


def day(start: datetime, n: int = 288, drift_t101: float = 0.0, excursion_p101: int | None = None):
    rows = []
    for i in range(n):
        t = start + timedelta(minutes=5 * i)
        for sid, unit, mu, sd in SENSORS:
            v = mu + sd * rng.normal()
            if sid == "T101":
                v += drift_t101 * i / n
            if sid == "P101" and excursion_p101 is not None and excursion_p101 <= i < excursion_p101 + 6:
                v += 7.0
            rows.append((t, sid, v, unit))
    return rows


def write(path, rows, header=("timestamp", "sensor_id", "reading", "unit"), newline="\n", bom=False):
    lines = [",".join(header)] + [f"{t:%Y-%m-%d %H:%M:%S},{sid},{v:.3f},{unit}" for t, sid, v, unit in rows]
    text = newline.join(lines) + newline
    path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8"))
    print(f"{path.relative_to(ROOT.parent)}: {len(rows)} rows")


d1 = day(datetime(2026, 3, 2))
write(ROOT / "clean" / "sensor_day1.csv", d1)
write(ROOT / "clean" / "sensor_day2.csv", day(datetime(2026, 3, 3), drift_t101=4.0, excursion_p101=150))

# corrupted day 1
lines = ["timestamp,sensor_id,Reading,unit"]
for k, (t, sid, v, unit) in enumerate(d1):
    val = f"{v:.3f}"
    ts = f"{t:%Y-%m-%d %H:%M:%S}"
    if k == 17:
        val = "N/A"
    if k == 41:
        val = ""
    if k == 77:
        val = f"{v:.3f}".replace(".", ",")
    if k == 120:
        ts = f"{t:%Y-%m-%dT%H:%M:%S}"
    if k == 198:
        val = "9999.0"  # T101: a stuck sensor value
    if k == 260:
        unit = "degF"
    lines.append(f"{ts},{sid},{val},{unit}")
    if k == 99:
        lines.append("")  # blank line
    if k == 150:
        lines.append(lines[-1])  # duplicated row
text = "\r\n".join(lines) + "\r\n"
p = ROOT / "corrupted" / "sensor_day1_corrupted.csv"
p.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))
print(f"{p.relative_to(ROOT.parent)}: {len(lines) - 1} rows (corrupted)")

write(
    ROOT / "corrupted" / "sensor_missing_column.csv",
    [(t, sid, v, "") for t, sid, v, _ in d1[:50]],
    header=("timestamp", "sensor_id", "reading"),
)
(ROOT / "corrupted" / "sensor_missing_column.csv").write_text(
    "\n".join(
        line.rsplit(",", 1)[0] for line in (ROOT / "corrupted" / "sensor_missing_column.csv").read_text().splitlines()
    )
    + "\n"
)
(ROOT / "corrupted" / "sensor_empty.csv").write_text("timestamp,sensor_id,reading,unit\n")
print("datasets/corrupted/sensor_empty.csv: 0 rows")

cal = np.linspace(0, 1000, 11)
(ROOT / "clean" / "calibration.csv").write_text(
    "reading_kpa,reference_kpa\n" + "\n".join(f"{x:.1f},{x * 1.02 - 3.0:.2f}" for x in cal) + "\n"
)
print("datasets/clean/calibration.csv: 11 rows")

big = []
for d in range(30):
    big += day(datetime(2026, 3, 2) + timedelta(days=d))
write(ROOT / "clean" / "large_day.csv", big)
