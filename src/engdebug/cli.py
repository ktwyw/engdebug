"""Command-line entry point: ``python -m engdebug.cli datasets/clean/sensor_day1.csv``."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from . import logsetup, pipeline
from .exceptions import PipelineError


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run the engdebug sensor pipeline on a CSV file.")
    parser.add_argument("path")
    parser.add_argument("--report", default=None, help="write the text report to this path")
    parser.add_argument("--strict", action="store_true", help="stop at the first bad row or record")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--json-logs", action="store_true", help="emit one JSON object per log line")
    args = parser.parse_args(argv)
    logsetup.configure(
        logging.DEBUG if args.verbose else logging.INFO, json_lines=args.json_logs, run_id=Path(args.path).stem
    )
    try:
        result = pipeline.run(
            args.path, {"skip_bad_rows": not args.strict, "strict_validation": args.strict}, args.report
        )
    except PipelineError as exc:
        logging.getLogger("engdebug").error("%s", exc)
        return 1
    sys.stdout.write(result["report"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
