# Chapter 4 · Data: files, encodings and validation

*For lab 04. Runnable example: `examples/ch04_csv_pitfalls.py`.*

## Why data is where most bugs live

Code is written once and read by a parser that rejects anything malformed. Data is produced by
instruments, vendors, spreadsheets and people, none of whom read your assumptions. A function that
works on the file you wrote it against will meet, within a month, a file that "looks the same" and is
not. This chapter is about the ways a simple text file can differ from what you expected, and about the
one habit that makes all of them harmless: a written contract, checked at the boundary.

## Text files are bytes

A file is a sequence of bytes. To get text from it, Python needs to know the *encoding*: the rule that
maps bytes to characters. UTF-8 is the modern default; Windows tools sometimes write "cp1252"
(Latin-style) and sometimes prefix UTF-8 files with a *byte-order mark* (BOM), three bytes `EF BB BF`
that are invisible in editors and that Python, reading as plain UTF-8, turns into the character
`\ufeff` glued to the first field. That is how a header that plainly says `timestamp` produces
`KeyError: 'timestamp'`: the key is actually `'\ufefftimestamp'`.

```python
open(path, encoding="utf-8")       # the BOM becomes part of the first header name
open(path, encoding="utf-8-sig")   # 'sig' = strip the signature if present; otherwise identical
```

Always pass `encoding=` explicitly. The default depends on the operating system and on environment
variables, which is a way of saying your program behaves differently on your colleague's machine.

To see what is really in a file, look at the bytes, not the editor's rendering:

```bash
head -c 64 file.csv | od -c          # macOS/Linux: shows \357\273\277 for a BOM, \r\n for CRLF
python -c "print(open('file.csv','rb').read(64))"   # anywhere
```

## Line endings

Unix files end lines with `\n`; Windows with `\r\n`. Python's text mode normalises this when reading -
*unless* you are using the `csv` module, which wants `newline=""` so that it can handle quoted fields
containing line breaks itself. The rule has no exceptions: `open(path, newline="")` whenever a csv
reader or writer is involved.

## The csv module, not `split(",")`

`line.split(",")` fails the first time a field contains a comma inside quotes (`"6,25"`), a quoted
header, or a trailing comma. The `csv` module handles the format's rules; `csv.DictReader` gives you a
dict per row keyed by the header:

```python
import csv
with open(path, encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f):
        row["reading"]        # a string; everything from a CSV is a string
```

Everything is a string until you convert it. The conversion is where the data's problems surface, so it
belongs in a function of its own with a clear error:

```python
def parse_reading(text):
    cleaned = text.strip().replace(",", ".")          # repair: a decimal comma is unambiguous here
    if cleaned.upper() in {"", "N/A", "NA", "NAN", "NULL", "-"}:
        raise ValueError(f"missing reading {text!r}")  # reject: there is no number to recover
    return float(cleaned)
```

## The catalogue of surprises

Lab 04's corrupted file contains all of these; each is a real thing a real vendor has sent.

| what | how it looks | what it breaks | the fix |
|---|---|---|---|
| byte-order mark | invisible | header lookup | `encoding="utf-8-sig"` |
| CRLF line endings | invisible | csv parsing of quoted fields | `newline=""` |
| header case | `Reading` vs `reading` | key lookup | normalise: `.strip().lower()` |
| blank lines | empty rows | `float("")` | skip rows with no content |
| placeholders | `N/A`, `NULL`, `-`, empty | `float()` | reject with the row number |
| decimal comma | `6,25` | `float()`; or, unquoted, the row splits into one extra field | repair if quoted; reject if the row is damaged |
| a second date format | `2026-03-02T00:05:00` | `strptime` | try the known formats in turn |
| duplicated rows | identical lines | double counting; "timestamps not increasing" | detect and drop, with a count |
| impossible values | 9999 degC | every downstream statistic | range check per unit |
| unknown unit | `degF` | `KeyError` in a lookup table | reject, name the known units |
| wrong column count | a missing or extra comma | misaligned fields | the csv reader's `restkey`/`None` values; validate the field count |
| leading/trailing spaces | ` T101` | lookups and joins | `.strip()` everything |

## Repair or reject?

Repair when the intended value is unambiguous and the repair is documented: a decimal comma inside a
quoted field, surrounding whitespace, header case. Reject when there is no single right answer: a
placeholder (what number is `N/A`?), an impossible value (9999 degC is a stuck sensor, not a
measurement), a row with the wrong number of fields. Never repair silently - a skipped row is reported
with its number and reason, every time, so that a file with 40 % missing readings cannot pass as a quiet
success. And never *invent*: filling a missing reading with 0 or with the previous value is an analysis
decision that belongs in the analysis, labelled, not in the parser.

## The input contract

Write down, before parsing anything, what a valid record *is*. In the reference pipeline it is one
dictionary and one table at the top of `validation.py`:

```python
SCHEMA = {"timestamp": datetime, "sensor_id": str, "reading": float, "unit": str}
RANGES = {"degC": (-50.0, 400.0), "bar": (0.0, 50.0), ...}
```

Then one function checks every record against it and raises `ValidationError` with the field, the row
and the value. Everything downstream can assume a valid record and needs no defensive code: the
calculations in `calculations.py` do not check for `None` or strings because nothing of the kind can
reach them. **Validate at the boundary, trust inside.** Validation scattered through the code is
validation that is missing somewhere.

Two details that matter: ranges are *inclusive* at both ends unless physics says otherwise (0.0 bar is a
valid gauge pressure), and an unknown unit is a rejection with a message listing the known ones, not a
`KeyError` from a lookup table.

## Dates and times

`datetime.strptime(text, "%Y-%m-%d %H:%M:%S")` parses one exact format. Loggers produce several; try
each in turn and raise with the text when none matches. Store `datetime` objects, not strings, so that
comparison and sorting work (as strings, `"2026-3-2"` sorts after `"2026-10-1"`). Beware of time zones
and daylight-saving changes; a plant that logs in local time has one hour a year with duplicate
timestamps and one with a gap - which the "timestamps must increase" check will find for you.

## Paths

Use `pathlib.Path`, not string concatenation: `Path("datasets") / "clean" / "day1.csv"` is correct on
every operating system; `"datasets/" + name` is not. Chapter 11 covers *where* a relative path points.

## Habits this chapter starts

- **Encoding and newline, always explicit.** `open(path, encoding="utf-8-sig", newline="")` for any CSV.
- **One function per conversion.** `parse_reading`, `parse_timestamp`: small, tested on every variant you
  have seen, with a message that names the value.
- **Write the contract first.** Schema and ranges in one place; one validator; nothing downstream checks
  again.
- **Report every skipped row.** Count them, log them, return them. Silence is the bug.
- **Keep the bad file.** Every corrupted file that broke the parser goes into `datasets/corrupted/` with a
  test that loads it. Your test data is the history of what the world has sent you.

Next: [Chapter 5 · Logic and numbers](05_logic_and_numbers.md).
