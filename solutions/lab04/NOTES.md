# Lab 04 solution notes

| symptom | cause | where |
|---|---|---|
| `KeyError: 'timestamp'` on a file whose header says timestamp | UTF-8 BOM glued to the first column name | first 3 bytes |
| header keys not found | `Reading` capitalised | header |
| `ValueError: could not convert string to float: 'N/A'` | placeholder | row 19 |
| `... : ''` | empty cell | row 43 |
| `ValueError: ... '6,958'` or wrong split | decimal comma (and, unquoted, an extra CSV field) | row 79 |
| `time data ... does not match format` | second timestamp format | row 122 |
| `KeyError: 'degF'` in validate | unknown unit | row 262 |
| 9999 degC accepted | no range check / exclusive bounds | row 200 |
| row counted twice | duplicated row | row 152 |

The unquoted decimal comma in the corrupted file splits into two fields: `reading` becomes `6` and
`unit` becomes `958`. The parser cannot repair that; it is rejected at validation as an unknown unit -
a genuine case where the only fix is upstream, with the vendor.

Blank lines are skipped; placeholders become problems with a row number; the two timestamp formats are
tried in turn; bounds are inclusive; an unknown unit is a rejection, not a crash.
