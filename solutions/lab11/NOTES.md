# Lab 11 solution notes

- ruff: `os` and `math`, `timedelta` unused (F401); imports unsorted (I001); the `format_duration`
  docstring over 120 characters (E501) - wrapped.
- mypy --strict: `hours_between` annotated `-> int` returned `float`. The annotation was right and the
  code wrong: "whole hours" means `int(total_seconds() // 3600)`. The report line "2.75 h 45 min" was the
  same bug seen by a human.
- tests: `shift_for` at 22:00 - the buggy `elif hour < 22` made 22:00 night; the docstring and test say
  the evening shift ends at 22, so night starts at 22: `hour < 22` is right for *evening*, and the fallthrough
  returns night. (No change needed there once the chain is read carefully; the test documents the boundary.)
- `report([])` crashed on `min([])`: guard with a conditional.

Commit messages, one per job: `style: remove unused imports and sort`, `fix: hours_between returns whole
hours (int) as documented`, `fix: report handles an empty day`.
