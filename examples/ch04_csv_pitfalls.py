"""Chapter 4: the byte-order mark, CRLF and a decimal comma, and how to open a CSV correctly.
Run:  python examples/ch04_csv_pitfalls.py"""

import csv
from pathlib import Path

p = Path("pitfalls.csv")
p.write_bytes(b'\xef\xbb\xbftimestamp,sensor_id,reading,unit\r\n2026-03-02 00:00:00,T101,"70,5",degC\r\n')

print("first bytes:", p.read_bytes()[:8])

with open(p, encoding="utf-8", newline="") as f:  # WRONG encoding for a BOM file
    row = next(csv.DictReader(f))
    print("keys read as utf-8:    ", list(row))  # the first key carries '\\ufeff'

with open(p, encoding="utf-8-sig", newline="") as f:  # RIGHT
    row = next(csv.DictReader(f))
    print("keys read as utf-8-sig:", list(row))
    text = row["reading"]
    print("reading as text:", repr(text), "-> float:", float(text.replace(",", ".")))

p.unlink()
