"""Glue: run the two stages on a file. Crashes since the ingestion rewrite."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import analyse  # noqa: E402
import ingest  # noqa: E402

CONFIG = {"thresholds": {"degC": 120.0, "bar": 12.0, "kPa": 1200.0, "kW": 900.0, "rpm": 3600.0}}


def main(path):
    records = ingest.load(path)
    means = analyse.sensor_means(records)
    found = analyse.alerts(records, CONFIG)
    return means, found


if __name__ == "__main__":
    print(main(sys.argv[1]))
