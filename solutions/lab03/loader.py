"""Load a readings file (fixed): errors are raised with context, never printed or swallowed."""

import csv


class LoaderError(Exception):
    """Base class for everything this loader raises on purpose."""


class BadRowError(LoaderError):
    """A row could not be parsed; carries the row number and the offending value."""

    def __init__(self, path, row, value, reason):
        self.path, self.row, self.value = str(path), row, value
        super().__init__(f"{path}, row {row}: {reason} (value {value!r})")


def load(path):
    try:
        f = open(path, encoding="utf-8-sig", newline="")
    except OSError as exc:
        raise LoaderError(f"cannot open {path}: {exc.strerror}") from exc
    readings = []
    with f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or "reading" not in reader.fieldnames:
            raise LoaderError(f"{path}: no 'reading' column; found {reader.fieldnames}")
        for row_number, row in enumerate(reader, start=2):
            try:
                readings.append(float(row["reading"]))
            except ValueError as exc:
                raise BadRowError(path, row_number, row["reading"], "reading is not a number") from exc
    return readings


def mean_reading(path):
    readings = load(path)
    if not readings:
        raise LoaderError(f"{path}: no readings to average")
    return sum(readings) / len(readings)
