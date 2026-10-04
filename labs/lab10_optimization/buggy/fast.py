"""Your optimised version. It must produce exactly the same output as slow.run and be measurably faster.
Start by copying slow.py's functions here and change one at a time, re-running the tests after each."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from slow import anomaly_scores, flagged, load, mean, readings_for, sensor_ids, std  # noqa: F401


def run(path):
    return flagged(load(path))
