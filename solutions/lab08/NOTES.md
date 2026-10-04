# Lab 08 solution notes

Two silent failures, found by logging rather than by reading:

- `LIMITS.get(rec["unit"], float("inf"))`: the table's keys had been lower-cased (`degc`) while the data say
  `degC`, so every temperature reading was compared with infinity. A DEBUG line printing the limit per
  record showed `inf` immediately. Now an unknown unit is a WARNING, logged once, and the reading is
  skipped visibly.
- `except Exception: pass` around the drift calculation hid the `KeyError` for S102, which was missing
  from `REFERENCES`. Now a missing reference is a WARNING naming the sensor.

The INFO lines with counts (`loaded 1728 records`, `9 threshold alerts`, `1 drift alerts`) make "it did
nothing" diagnosable in ten seconds: whichever count is missing or zero points at the stage.

Diagnostic playbook, when the monitor reports nothing: (1) is the `loaded N records` line there and N
right? (2) any `no limit configured` warnings? (3) any `no reference value` warnings?
