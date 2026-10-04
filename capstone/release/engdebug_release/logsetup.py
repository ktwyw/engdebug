"""Structured logging for the pipeline: one call configures a console handler with a consistent format.

Use ``logging.getLogger(__name__)`` in each module; never ``print`` from library code. Log at DEBUG for
details useful when diagnosing, INFO for the normal milestones, WARNING for recoverable problems (a
skipped row), ERROR for failures that stop a step.
"""

from __future__ import annotations

import logging
import sys

FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"


def configure(level: int = logging.INFO, stream=None) -> logging.Logger:
    root = logging.getLogger("engdebug_release")
    root.setLevel(level)
    if not root.handlers:
        handler = logging.StreamHandler(stream or sys.stderr)
        handler.setFormatter(logging.Formatter(FORMAT, datefmt="%H:%M:%S"))
        root.addHandler(handler)
    return root
