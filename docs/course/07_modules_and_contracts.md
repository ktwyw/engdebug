# Chapter 7 · Modules, contracts and integration

*For lab 07.*

## Programs are made of parts

A program larger than a page is split into modules: files, each with one job. The pipeline has one for
reading files, one for validating, one for calculating, one for alerting, one for reporting, and one
that strings them together. Each can be understood, tested and replaced on its own.

Splitting creates *boundaries*, and a boundary is a place where two modules must agree about the shape
of the data crossing it. When they stop agreeing - because one was changed without the other - each
module's own tests stay green and the program breaks. That is an *integration bug*, and it is the
subject of lab 07.

## Imports

`import csv` makes the standard library's csv module available as `csv`. `from .exceptions import
IngestionError` imports one name from a sibling module in the same package (the leading dot means
"relative to this package"). Python finds modules by searching `sys.path`: the directory of the script
being run, then the installed packages of the active environment. "`ModuleNotFoundError` on my
colleague's machine" is nearly always a different `sys.path` - a different working directory or a
different environment (chapter 11).

A *package* is a directory with an `__init__.py`; `src/engdebug/` is one. `pip install -e .` registers
it so that `import engdebug` works from anywhere in the environment, regardless of the working directory.
Two modules importing each other in a circle is an `ImportError` at startup; the fix is usually a third
module both can import.

## The interface contract

Every function has a contract: what it accepts, what it returns, what it raises. The contract lives in
three places that must agree:

1. **The signature and type hints**: `def load(path: Path) -> list[dict]:`. Tools check these (chapter 10).
2. **The docstring**: the shape in words. "Returns a list of records, one per data row, each a dict with
   keys `timestamp` (datetime), `sensor_id` (str), `reading` (float), `unit` (str). Raises
   `IngestionError` for a missing file or column."
3. **The tests**: `test_load_returns_list_of_records_with_float_readings`.

Lab 07's first bug is a function whose contract changed - a list of rows became a dict of columns - while
the docstring, the hints and the consumer did not. The `TypeError` appears in the consumer, two frames
from the cause; the fix is to decide the contract, write it down, and test it *at the boundary*.

## Integration tests live at the boundary

```python
def test_analysis_consumes_what_ingestion_produces():
    records = ingest.load(DATA / "clean" / "sensor_day1.csv")   # real data
    means = analyse.sensor_means(records)                       # the next stage
    assert set(means) == {"T101", "P101", ...}
```

One test like this per boundary would have caught the rewrite the day it was made. It runs both stages
on a real file, so it also catches the problems unit tests with hand-made inputs miss: the real file has
a BOM, the real timestamps are strings until someone parses them. The reference pipeline's
`tests/integration/test_pipeline.py` runs every stage on the clean and the corrupted files.

## Configuration is an interface too

`run.py` says `thresholds`; `analyse.py` reads `threshold`. Nothing checks the agreement until runtime.
Rules that prevent configuration drift:

- one definition: a `DEFAULT_CONFIG` dict in one module, and every reader imports it or is given it;
- validated on entry: `load_config` rejects unknown keys ("did you mean `thresholds`?") and bad values,
  with a message listing what is known;
- typed: values converted (`float`) and checked (`max_drift > 0`) once, at load time, not at each use.

The reference `pipeline.load_config` is twelve lines and would have made lab 07's second bug an error
message with the answer in it.

## Designing a boundary

- **Return plain data at boundaries**: lists, dicts, dataclasses, `datetime`, `float` - not half-processed
  strings, not objects only the producer understands.
- **Convert and validate before the boundary**, so the consumer can trust what it receives (chapter 4).
- **Change a contract in one commit** that changes the producer, the consumer, the docstring and the
  test together; a contract changed in one place is a bug scheduled for later.
- **Prefer rows (a list of records) for streaming and validation; columns (a dict of lists, or arrays)
  for numerical work** - and convert between them in one named function, not implicitly.

## Reading code you did not write

Lab 07 is also the first lab where the bug is in someone else's design. A method:

1. Start from the entry point (`run.py`, `main`) and follow the calls; draw the boxes and the arrows.
2. At each arrow, write the shape of the data: "list of dicts with keys ...".
3. Where two adjacent notes disagree, you have found the bug - without reading any function body.

`type(x)` and `x[:2]` printed at a boundary answer most questions faster than reading the producer.

## Habits this chapter starts

- **Every public function has a docstring that states what it returns and what it raises.** If you
  cannot write the sentence, the function does too much.
- **Type hints on every signature**, so a tool can check the contract (chapter 10).
- **One integration test per boundary**, on real data.
- **Configuration defined once, validated on load.**
- **Run the whole program, not only the tests, after changing a shape.** Unit tests are blind to boundaries.

Next: [Chapter 8 · Logging and observability](08_logging.md).
