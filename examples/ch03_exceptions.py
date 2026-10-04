"""Chapter 3: the four parts of try, a custom exception with context, and chaining.
Run:  python examples/ch03_exceptions.py"""

from pathlib import Path


class LoaderError(Exception):
    """Base class for everything the loader raises on purpose."""


class BadRowError(LoaderError):
    def __init__(self, path, row, value):
        self.row, self.value = row, value
        super().__init__(f"{path}, row {row}: reading is not a number (value {value!r})")


def load(path):
    try:
        f = open(path, encoding="utf-8")
    except FileNotFoundError as exc:  # translate, with context, keep the original
        raise LoaderError(f"cannot open {path}") from exc
    with f:
        readings = []
        for row, line in enumerate(f, start=1):
            text = line.strip()
            try:
                readings.append(float(text))
            except ValueError as exc:
                raise BadRowError(path, row, text) from exc
        return readings


if __name__ == "__main__":
    p = Path("readings.txt")
    p.write_text("70.0\n71.5\nN/A\n")
    try:
        load(p)
    except BadRowError as exc:
        print("caught:", exc)
        print("row:", exc.row, "value:", repr(exc.value))
        print("original cause:", repr(exc.__cause__))
    try:
        load("nope.txt")
    except LoaderError as exc:
        print("caught:", exc)
    p.unlink()
