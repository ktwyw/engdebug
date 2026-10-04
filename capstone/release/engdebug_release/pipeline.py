"""The end-to-end run: ingest -> validate -> group -> calculate -> alert -> report."""

from __future__ import annotations

import logging
from pathlib import Path

from . import alerting, ingestion, reporting, validation
from .exceptions import ConfigError

log = logging.getLogger("engdebug_release.pipeline")

DEFAULT_CONFIG = {
    "skip_bad_rows": True,
    "strict_validation": False,
    "thresholds": None,
    "references": {},
    "max_drift": 2.0,
    "z_limit": 4.0,
    "anomaly_window": 20,
}


def load_config(overrides: dict | None = None) -> dict:
    cfg = dict(DEFAULT_CONFIG)
    for key, value in (overrides or {}).items():
        if key not in DEFAULT_CONFIG:
            raise ConfigError(f"unknown configuration key {key!r}; known: {sorted(DEFAULT_CONFIG)}")
        cfg[key] = value
    if cfg["max_drift"] <= 0:
        raise ConfigError("max_drift must be positive")
    return cfg


def run(path, config: dict | None = None, report_path=None) -> dict:
    """Run the pipeline on one file; return the summary rows, alerts, rejected rows and the report text."""
    cfg = load_config(config)
    bad_rows: list = []
    records = ingestion.load_readings(path, skip_bad_rows=cfg["skip_bad_rows"], bad_rows=bad_rows)
    log.info("loaded %d records from %s (%d rows skipped)", len(records), Path(path).name, len(bad_rows))
    for row, reason in bad_rows:
        log.warning("skipped row %d: %s", row, reason)
    good, rejected = validation.validate_all(records, strict=cfg["strict_validation"])
    for row, reason in rejected:
        log.warning("rejected record %d: %s", row, reason)
    good, n_dup = ingestion.drop_duplicates(good)
    if n_dup:
        log.warning("dropped %d duplicate records", n_dup)
    groups = ingestion.group_by_sensor(good)
    for sensor_id, recs in groups.items():
        validation.check_monotonic_timestamps(recs)
    alerts = alerting.threshold_alerts(good, cfg["thresholds"])
    alerts += alerting.drift_alerts(groups, cfg["references"], cfg["max_drift"])
    alerts += alerting.anomaly_alerts(groups, cfg["z_limit"], cfg["anomaly_window"])
    alerts.sort(key=lambda a: a["timestamp"])
    rows = reporting.summarise(groups)
    text = reporting.text_report(rows, alerts)
    if report_path is not None:
        reporting.write_report(text, report_path)
        log.info("report written to %s", report_path)
    log.info("%d sensors, %d alerts", len(rows), len(alerts))
    return {"summary": rows, "alerts": alerts, "skipped": bad_rows, "rejected": rejected, "duplicates": n_dup, "report": text}
