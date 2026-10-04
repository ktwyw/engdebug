"""Structured logging for the pipeline: one call configures a console handler with a consistent format.

Use ``logging.getLogger(__name__)`` in each module; never ``print`` from library code. Log at DEBUG for
details useful when diagnosing, INFO for the normal milestones, WARNING for recoverable problems (a
skipped row), ERROR for failures that stop a step.
"""

from __future__ import annotations

import json
import logging
import sys

FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"


class JsonFormatter(logging.Formatter):
    """One JSON object per line: what log aggregators (and grep) want. `run_id` is added when configured."""

    def __init__(self, run_id: str | None = None):
        super().__init__()
        self.run_id = run_id

    def format(self, record: logging.LogRecord) -> str:
        doc = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if self.run_id is not None:
            doc["run_id"] = self.run_id
        if record.exc_info:
            doc["exception"] = self.formatException(record.exc_info)
        return json.dumps(doc)


def configure(
    level: int = logging.INFO, stream=None, json_lines: bool = False, run_id: str | None = None
) -> logging.Logger:
    """Configure the package logger once. json_lines=True emits structured JSON with an optional run id."""
    root = logging.getLogger("engdebug")
    root.setLevel(level)
    if not root.handlers:
        handler = logging.StreamHandler(stream or sys.stderr)
        handler.setFormatter(JsonFormatter(run_id) if json_lines else logging.Formatter(FORMAT, datefmt="%H:%M:%S"))
        root.addHandler(handler)
    return root
