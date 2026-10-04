# Lab 06 · Class design: shared state and missing invariants

**Context.** Two symptoms from the same module. Pump 2's dashboard shows pump 1's readings. A pump that
had tripped to `fault` was set to `running` by a script, skipping the inspection, and ran for a shift
before anyone noticed. Both are design bugs in `equipment.py`: state is shared where it should be private,
and rules that exist on paper are not in the code.

**Time.** 60 minutes. **Prerequisites.** Labs 01-05; basic classes.

## What you will learn

- the mutable default argument trap (`readings=[]`) and why it is Python's most famous bug
- the difference between a class attribute and an instance attribute (`history = []` at class level is
  one list for every sensor)
- *invariants*: statements that must always be true of an object (readings in time order, status in the
  allowed set), and that the object itself must enforce
- why `__eq__` without `__hash__` makes objects unusable in sets and dicts, and why comparing with the
  wrong type must return `False` rather than crash

## Reproduce

```bash
python -c "
import sys; sys.path.insert(0, 'labs/lab06_class_design/buggy'); from equipment import Sensor
from datetime import datetime
a, b = Sensor('A', 'degC'), Sensor('B', 'degC'); a.add(datetime(2026, 3, 2), 1.0)
print('B readings:', b.readings)     # expect []
print('B history:', b.history)       # expect []
"
python -m pytest labs/lab06_class_design -q
```

## Diagnose

Use `id()` to prove the sharing: `id(a.readings) == id(b.readings)`. Then read the class body and find
every piece of state and ask, for each: is this per instance or per class? created once or per call?
Then read `set_status` and ask what it checks. Nothing - that is the second bug.

## Fix

1. `readings=None` in the signature and `self.readings = readings if readings is not None else []`
   (or a `dataclass` with `field(default_factory=list)`).
2. `self.history = []` in `__init__`, not at class level.
3. `latest` returns `None` for an empty sensor; `mean` raises `ValueError` - decide which is right for
   each and say why (hint: a missing latest value is normal before the first reading; a mean of nothing is
   a mistake in the caller).
4. `add` rejects a timestamp not after the last one.
5. `set_status` checks the new status against a table of allowed transitions
   (`fault → maintenance | stopped`, never `fault → running`) and raises with a message naming both states.
6. `attach` rejects a duplicate sensor id.
7. Add `__hash__` consistent with `__eq__`, and make `__eq__` return `NotImplemented` for other types.

## Prevent recurrence

`ruff` rule B006 catches mutable defaults. For everything else: when a class has a rule, write it as a
test (`test_status_transitions_are_enforced`) before you write the method. The reference `models.py` uses
a dataclass for `Sensor` and a transition table for `Equipment`.

## Hint ladder

Use one hint at a time, only after an honest attempt.

1. `id(a.readings) == id(b.readings)` - run it.
2. Where is `history` defined: in the class body or in `__init__`? Which one is shared?
3. A transition table: a dict from status to the set of statuses allowed next; `set_status` checks it before assigning.

## Deliverable

The fixed `equipment.py` (tests green) and a list of the invariants of each class, one line each, as you
would put them in the docstring.
