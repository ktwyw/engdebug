"""Analysis stage: still expects a list of row dicts from the ingestion stage."""


def sensor_means(records):
    totals, counts = {}, {}
    for rec in records:
        sid = rec["sensor_id"]
        totals[sid] = totals.get(sid, 0.0) + rec["reading"]
        counts[sid] = counts.get(sid, 0) + 1
    return {sid: totals[sid] / counts[sid] for sid in totals}


def alerts(records, config):
    out = []
    for rec in records:
        limit = config["threshold"][rec["unit"]]
        if rec["reading"] > limit:
            out.append((rec["sensor_id"], rec["reading"]))
    return out
