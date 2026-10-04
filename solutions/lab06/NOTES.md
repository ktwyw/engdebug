# Lab 06 solution notes

- `readings=[]` is evaluated once, when `def` runs: every sensor created without readings shares one list.
  `id(a.readings) == id(b.readings)` proves it. Use `None` and create the list inside.
- `history = []` in the class body is a class attribute: one list for all instances. Per-instance state
  goes in `__init__`.
- `latest()` of an empty sensor returns `None` (not having a reading yet is normal); `mean()` raises
  (averaging nothing is the caller's error). Both are documented choices, not accidents.
- `set_status` enforces a transition table; `fault -> running` is now impossible by construction.
- `__eq__` without `__hash__` sets `__hash__ = None`, so the object cannot go in a set; defining both
  on the same field keeps them consistent. Returning `NotImplemented` for foreign types lets Python fall
  back to `False` instead of raising `AttributeError`.
