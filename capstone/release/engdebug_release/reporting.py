"""Daily summary reports: a text table for humans and JSON for machines."""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

from .calculations import mean_and_std


def summarise(groups: dict[str, list[dict]]) -> list[dict]:
    """Per-sensor summary rows: count, mean, std, min, max, first and last timestamp."""
    rows = []
    for sensor_id in sorted(groups):
        recs = groups[sensor_id]
        vals = [r["reading"] for r in recs]
        m, s = mean_and_std(vals)
        rows.append({"sensor_id": sensor_id, "unit": recs[0]["unit"], "n": len(vals), "mean": m, "std": s, "min": min(vals), "max": max(vals), "first": recs[0]["timestamp"], "last": recs[-1]["timestamp"]})
    return rows


def text_report(rows: list[dict], alerts: list[dict], title: str = "Daily summary") -> str:
    lines = [title, "=" * len(title), "", f"{'sensor':<10}{'unit':<6}{'n':>5}{'mean':>12}{'std':>10}{'min':>10}{'max':>10}"]
    for r in rows:
        lines.append(f"{r['sensor_id']:<10}{r['unit']:<6}{r['n']:>5}{r['mean']:>12.3f}{r['std']:>10.3f}{r['min']:>10.3f}{r['max']:>10.3f}")
    lines += ["", f"Alerts: {len(alerts)}"]
    for a in alerts:
        lines.append(f"  {a['timestamp']:%Y-%m-%d %H:%M}  {a['sensor_id']:<8} {a['kind']:<8} value={a['value']:.3f} limit={a['limit']}")
    return "\n".join(lines) + "\n"


def _json_default(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"not JSON serialisable: {type(obj).__name__}")


def json_report(rows: list[dict], alerts: list[dict]) -> str:
    return json.dumps({"summary": rows, "alerts": alerts}, default=_json_default, indent=2)


def write_report(text: str, path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path
