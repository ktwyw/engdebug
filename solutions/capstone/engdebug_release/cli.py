"""Command-line entry point: ``python -m engdebug_release.cli datasets/clean/sensor_day1.csv``."""

from __future__ import annotations

import argparse
import logging
import sys

from . import logsetup, pipeline
from .exceptions import PipelineError


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run the engdebug_release sensor pipeline on a CSV file.")
    parser.add_argument("path")
    parser.add_argument("--report", default=None, help="write the text report to this path")
    parser.add_argument("--strict", action="store_true", help="stop at the first bad row or record")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)
    logsetup.configure(logging.DEBUG if args.verbose else logging.INFO)
    try:
        result = pipeline.run(args.path, {"skip_bad_rows": not args.strict, "strict_validation": args.strict}, args.report)
    except PipelineError as exc:
        logging.getLogger("engdebug_release").error("%s", exc)
        return 1
    sys.stdout.write(result["report"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
