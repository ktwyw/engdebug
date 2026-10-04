# Reading the reference pipeline

This is the working version of the code the labs break. Read it in the order the data flows; each module
is short and has a docstring saying what it is for.

| order | module | what to look at |
|---|---|---|
| 1 | `exceptions.py` | a base class and one subclass per stage; every message carries context |
| 2 | `ingestion.py` | `load_readings`: the `open()` arguments, the header normalisation, the `try/except` per row that either raises with the row number or records the problem |
| 3 | `validation.py` | `SCHEMA` and `RANGES` at the top (the input contract), one validator, inclusive bounds |
| 4 | `calculations.py` | small pure functions; `moving_average` divides by the number of values present; `anomaly_scores` is deliberately simple (O(n*w)) because clarity wins at this size |
| 5 | `models.py` | `Sensor` as a dataclass with `default_factory=list`; `Equipment` with a transition table |
| 6 | `alerting.py` | thresholds validated before use (`_limits`); `abs()` on the drift |
| 7 | `reporting.py` | a text table and JSON with a `default=` for datetimes |
| 8 | `logsetup.py` | configure once; a plain and a JSON formatter |
| 9 | `pipeline.py` | the stages in order, a count logged after each, config validated on load |
| 10 | `cli.py` | arguments in, exit code out; the only place that prints |
| 11 | `engineering.py` | units in every name, SI inside, `convert` with sourced factors, a range check with a message per correlation; its V&V record is `tests/benchmarks/` |

Things a beginner may not have met, in the order they appear:

- `from __future__ import annotations` lets type hints use `list[dict]` and `int | None` on Python 3.10.
- `Path(path)` (pathlib) instead of string paths; `path.exists()`, `path.name`.
- `csv.DictReader` yields one dict per row keyed by the header; everything in it is a string.
- `enumerate(reader, start=2)` numbers rows from 2 because row 1 is the header.
- `raise IngestionError(...) from exc` keeps the original exception attached (chapter 3).
- `@dataclass` and `field(default_factory=list)` (chapter 6).
- `@property` makes a method readable like an attribute (`sensor.latest`).
- `logging.getLogger("engdebug.pipeline")` and `log.info("%d records", n)` (chapter 8).
- `json.dumps(..., default=_json_default)` tells JSON how to write a datetime.
- `if __name__ == "__main__":` runs `main()` only when the file is executed, not when imported.
