"""Daily monitor (fixed): exact configuration lookups, no swallowed errors, logging at every stage."""

import csv
import logging
from datetime import datetime

log = logging.getLogger(__name__)

LIMITS = {"degC": 120.0, "bar": 12.0, "kPa": 1200.0, "kW": 900.0, "rpm": 3600.0}
REFERENCES = {"T101": 72.0, "P101": 6.2, "W101": 340.0, "T102": 65.0, "P102": 610.0}  # S102 deliberately absent: see the WARNING


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        records = [{"timestamp": datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S"), "sensor_id": r["sensor_id"], "reading": float(r["reading"]), "unit": r["unit"]} for r in csv.DictReader(f)]
    log.info("loaded %d records from %s", len(records), path)
    return records


def threshold_alerts(records):
    out = []
    warned = set()
    for rec in records:
        unit = rec["unit"]
        if unit not in LIMITS:
            if unit not in warned:
                log.warning("no limit configured for unit %r (sensor %s): readings in this unit are not checked", unit, rec["sensor_id"])
                warned.add(unit)
            continue
        log.debug("%s %s reading %.3f limit %.3f", rec["sensor_id"], unit, rec["reading"], LIMITS[unit])
        if rec["reading"] > LIMITS[unit]:
            out.append((rec["sensor_id"], "high", rec["reading"]))
    log.info("%d threshold alerts", len(out))
    return out


def drift_alerts(records, max_drift=1.5):
    out = []
    by_sensor = {}
    for rec in records:
        by_sensor.setdefault(rec["sensor_id"], []).append(rec["reading"])
    for sid, values in by_sensor.items():
        if sid not in REFERENCES:
            log.warning("no reference value for sensor %s: drift not checked", sid)
            continue
        d = sum(values) / len(values) - REFERENCES[sid]
        log.debug("%s drift %.3f (limit %.3f)", sid, d, max_drift)
        if abs(d) > max_drift:
            out.append((sid, "drift", d))
    log.info("%d drift alerts", len(out))
    return out


def run(path):
    records = load(path)
    found = threshold_alerts(records) + drift_alerts(records)
    log.info("%d alerts in total", len(found))
    return found
