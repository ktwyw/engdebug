"""Analysis stage (fixed): consumes the list-of-records contract and validates its configuration."""


def sensor_means(records):
    if not isinstance(records, list):
        raise TypeError(f"records must be a list of dicts, got {type(records).__name__}")
    totals, counts = {}, {}
    for rec in records:
        sid = rec["sensor_id"]
        totals[sid] = totals.get(sid, 0.0) + rec["reading"]
        counts[sid] = counts.get(sid, 0) + 1
    return {sid: totals[sid] / counts[sid] for sid in totals}


def alerts(records, config):
    try:
        thresholds = config["thresholds"]
    except KeyError:
        raise KeyError(f"config lacks 'thresholds'; keys present: {sorted(config)}") from None
    out = []
    for rec in records:
        if rec["unit"] not in thresholds:
            raise KeyError(f"no threshold for unit {rec['unit']!r}; configured: {sorted(thresholds)}")
        if rec["reading"] > thresholds[rec["unit"]]:
            out.append((rec["sensor_id"], rec["reading"]))
    return out
