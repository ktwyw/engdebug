# Changelog

## 0.1.0 - 2026-10-04

First public release.

- **Reference pipeline** (`engdebug`, 10 modules, standard library only): ingestion with context-rich
  errors, schema and range validation, engineering calculations, Sensor/Equipment classes with
  invariants, alerting, reporting, structured logging, a CLI.
- **Tests** at every level: unit (with Hypothesis), integration on clean and corrupted data, end-to-end
  through the CLI, one regression test per lab, performance.
- **Labs** 01-11 and 13 with deliberately broken code, handouts in the reproduce-observe-diagnose-fix-prevent
  shape, failing tests, and worked solutions; a lab checker that proves each buggy version fails and each
  solution passes.
- **Capstone**: release candidate 0.2.0-rc1 with a data-handling bug, a logic bug and a 100x performance
  regression; acceptance tests; a worked postmortem.
- **Docs**: the debugging workflow, an error catalog, a testing guide, a performance playbook, a postmortem
  template, a 12-week syllabus, learning outcomes and rubrics, a course checklist.
- **Industrial workflow**: CI (tests across 3 OS x 4 Python versions, ruff, mypy, lab checker), issue and
  pull-request templates.
