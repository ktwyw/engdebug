# Lab 12 · Capstone: incident response

The capstone lives in [`capstone/`](../../capstone): a broken release candidate, three open incidents,
acceptance tests that fail, and a postmortem to write. See `capstone/README.md` for the brief and rules,
`docs/rubrics.md` for how it is graded, and `docs/incident_postmortem_template.md` for the write-up.

```bash
python -m pytest capstone/tests -q                       # fails on the release candidate
cp -r capstone/release my_release
ENGDEBUG_CAPSTONE_SRC=my_release python -m pytest capstone/tests -q
```

## Hint ladder

Use one hint at a time, only after an honest attempt.

1. One incident at a time; reproduce each with a command before reading any code.
2. INC-101: lab 04 (bytes). INC-102: lab 05 (sign). INC-103: lab 09 (profile a day, then look at the top function's loop).
3. The acceptance tests name the behaviour; your regression tests should name the cause.

