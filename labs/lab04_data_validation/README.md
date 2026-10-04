# Lab 04 · Dirty data: the file that "looks the same"

**Context.** The vendor's January file parsed perfectly. The March file -
`datasets/corrupted/sensor_day1_corrupted.csv` - crashes the parser, and when you force it through, the
numbers are wrong. Open it in a plain text editor (not a spreadsheet, which hides most of this) and look
at the first line, the line endings, the header, row 19, row 43, row 79, and row 122.

**Time.** 75 minutes. **Prerequisites.** Labs 01-03.

## What you will learn

- the ten ways a "simple CSV" differs from what you assumed: byte-order mark, Windows line endings, a
  capitalised header, blank lines, placeholders (`N/A`, empty), a decimal comma, a second timestamp format,
  duplicated rows, impossible values, unknown units
- the input contract: write down what a valid record *is* before parsing anything
- the difference between a row you must reject (and report) and one you can repair (a decimal comma)
- why boundaries are inclusive (a reading of exactly 0.0 bar is valid) and why `limits[rec["unit"]]`
  without a guard is a `KeyError` waiting for the first unknown unit

## Reproduce

```bash
python -m pytest labs/lab04_data_validation -q
file datasets/corrupted/sensor_day1_corrupted.csv       # "with BOM" and "CRLF line terminators" on Linux/macOS
head -c 60 datasets/corrupted/sensor_day1_corrupted.csv | od -c | head -3
```

## Diagnose

Work through the failures one at a time and keep a table: *symptom → cause → where in the file*. The
traceback for the BOM is the most instructive: `KeyError: 'timestamp'` on a file whose header plainly says
`timestamp` - until you look at the bytes.

## Fix

Give `parse_file` a `report_problems=False` keyword. When it is `True`, return `(records, problems)` where
`problems` is a list of `(row_number, reason)`; when `False`, raise on the first problem. Then:

1. open with `encoding="utf-8-sig"` (strips the BOM) and `newline=""` (lets the csv module handle CRLF);
2. normalise header names (`strip().lower()`);
3. skip blank lines;
4. parse the reading through a helper that accepts a decimal comma and rejects placeholders with a
   clear reason;
5. try the timestamp formats in turn;
6. in `validate`, make the boundaries inclusive and treat an unknown unit as a rejection, not a crash.

## Prevent recurrence

The input contract lives in one place (the reference package's `validation.py` has `SCHEMA` and `RANGES`
at the top) and every file goes through it. A sample of the vendor's *next* file goes into
`datasets/corrupted/` with a test the day it arrives. Never repair data silently: every skipped row is
reported with its number.

## Hint ladder

Use one hint at a time, only after an honest attempt.

1. `head -c 3 file | od -c` shows the first three bytes. What are they?
2. Row 19 and row 43 differ from the others in one cell; `float()` of what?
3. `encoding='utf-8-sig'`, `newline=''`, `.strip().lower()` on header names, `.replace(',', '.')` on readings, try the formats in a loop.

## Deliverable

The fixed `parse.py` (tests green) and your symptom → cause table. Bonus: a one-line shell command that
counts how many rows of the March file contain `N/A`.
