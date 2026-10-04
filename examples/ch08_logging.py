"""Chapter 8: logging instead of print; a silent default made visible.
Run:  python examples/ch08_logging.py          (INFO and above)
      python examples/ch08_logging.py debug    (everything)"""

import logging
import sys

log = logging.getLogger("example.monitor")

LIMITS = {"degc": 120.0, "bar": 12.0}  # the bug: keys in a different case from the data


def threshold_alerts(records):
    out = []
    for rec in records:
        limit = LIMITS.get(rec["unit"])
        if limit is None:
            log.warning("no limit configured for unit %r (sensor %s)", rec["unit"], rec["sensor_id"])
            continue
        log.debug("%s %s reading %.1f limit %.1f", rec["sensor_id"], rec["unit"], rec["reading"], limit)
        if rec["reading"] > limit:
            out.append(rec["sensor_id"])
    log.info("%d of %d readings over their limit", len(out), len(records))
    return out


if __name__ == "__main__":
    level = logging.DEBUG if "debug" in sys.argv[1:] else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)-8s %(name)s: %(message)s", datefmt="%H:%M:%S")
    records = [
        {"sensor_id": "T101", "unit": "degC", "reading": 130.0},
        {"sensor_id": "P101", "unit": "bar", "reading": 6.0},
    ]
    print("alerts:", threshold_alerts(records))
