# Chapter 6 · Classes and state

*For lab 06. Runnable example: `examples/ch06_mutable_default.py`.*

## Names, objects and references

The single most important fact about Python for this chapter: a variable is a *name bound to an
object*, not a box containing a value. Two names can be bound to the same object, and changing the
object through one name changes what the other sees.

```python
a = [1, 2]
b = a            # b is another name for the SAME list
b.append(3)
print(a)         # [1, 2, 3]
```

Lists, dicts and sets are *mutable*: they can be changed in place. Numbers, strings and tuples are
*immutable*: operations produce new objects. `id(x)` returns an object's identity; `a is b` tests
whether two names refer to the same object. Most state bugs in Python are two names sharing one mutable
object where the author assumed two objects.

## The mutable default argument

```python
class Sensor:
    def __init__(self, sensor_id, readings=[]):
        self.readings = readings
```

The default `[]` is evaluated **once**, when the `def` statement runs - not each time the function is
called. Every `Sensor()` created without a `readings` argument gets the *same* list. Add a reading to
one sensor and every sensor has it. This is lab 06's "pump 2 shows pump 1's readings", and it is the
most famous bug in Python because the code looks completely reasonable.

The idiom:

```python
    def __init__(self, sensor_id, readings=None):
        self.readings = list(readings) if readings is not None else []
```

`None` is immutable, so it is safe as a default; the fresh list is created inside the call. (`list(...)`
also copies a list the caller passed, so later changes to the caller's list do not leak in.) The linter
rule B006 catches the pattern; learn the idiom anyway.

## Class attributes and instance attributes

```python
class Sensor:
    history = []                  # ONE list, attached to the class, shared by all instances

    def __init__(self, sensor_id):
        self.sensor_id = sensor_id   # one per instance
```

Anything assigned in the class body belongs to the class. Reading `sensor.history` finds it through the
class; appending to it appends to the shared list. Per-instance state goes in `__init__` through `self`.
Class attributes are for genuine constants shared by all instances (`ALLOWED_TRANSITIONS`,
`KPA_PER_BAR`) - immutable ones, preferably.

## What a class is for: invariants

A class bundles data with the rules about that data. The rules are *invariants* - statements that must
be true of every instance at every moment:

- a sensor's readings are in strictly increasing time order;
- a piece of equipment's status is one of a known set, and changes only along allowed transitions;
- a sensor id is attached to at most one piece of equipment.

The class's job is to make the invariants impossible to violate from outside: every method that changes
state checks them and raises if the change would break one. If `Equipment.set_status` simply assigns,
the "no `fault → running` without maintenance" rule exists only on paper, and lab 06's second story
happens.

```python
ALLOWED = {"running": {"stopped", "fault"}, "stopped": {"running", "maintenance"},
           "maintenance": {"stopped"}, "fault": {"maintenance", "stopped"}}

def set_status(self, new):
    if new not in ALLOWED:
        raise ValueError(f"unknown status {new!r}")
    if new not in ALLOWED[self.status]:
        raise ValueError(f"{self.name}: cannot go from {self.status!r} to {new!r}")
    self.status = new
```

A transition *table* beats a chain of `if`s: it is data, it can be printed, tested exhaustively, and
changed without touching logic. Write the invariants in the class docstring; write a test per invariant.

## `None` is a value, not an error

`Sensor.latest()` on a sensor with no readings: return `None` or raise? Both can be right; the choice
must be deliberate and documented. "No reading yet" is a normal state of a new sensor - return `None`
and make callers handle it. "The mean of no readings" is a caller asking a question with no answer -
raise `ValueError`. What is never right is `self.readings[-1]` crashing with `IndexError` because nobody
thought about the empty case; that is the class failing to own its boundary.

## Equality and hashing

By default two objects are equal only if they are the same object. Defining `__eq__` changes that:

```python
def __eq__(self, other):
    if not isinstance(other, Equipment):
        return NotImplemented          # let Python try the other side, then fall back to False
    return self.name == other.name
```

Two rules. First, return `NotImplemented` (not `False`, and never crash) for a type you do not compare
with; `pump == "pump1"` must be `False`, not `AttributeError`. Second, **if you define `__eq__`, define
`__hash__`** on the same fields: Python sets `__hash__ = None` when a class defines only `__eq__`, which
makes instances unusable as dict keys or set members (`TypeError: unhashable type`). Equal objects must
hash equal.

## Dataclasses

For a class that is mostly data, `dataclasses` writes `__init__`, `__repr__` and `__eq__` for you and has
the right idiom for mutable defaults built in:

```python
from dataclasses import dataclass, field

@dataclass
class Sensor:
    sensor_id: str
    unit: str
    readings: list = field(default_factory=list)    # a fresh list per instance
```

`frozen=True` makes instances immutable (and hashable), which eliminates whole classes of state bugs
for objects that never need to change.

## Copies

`b = a` does not copy. `list(a)`, `a[:]`, `dict(a)` make *shallow* copies: a new container whose
elements are the same objects (fine for lists of numbers; a trap for lists of lists).
`copy.deepcopy(a)` copies all the way down. When a function receives a list and must not change the
caller's, copy it on the way in or do not mutate it at all.

## Habits this chapter starts

- **`None` as the default, create inside.** For every mutable default, every time.
- **State in `__init__`, constants in the class body.**
- **Invariants in the docstring and in tests**, enforced by the methods that change state.
- **Prefer immutable.** Tuples over lists for fixed collections; `frozen` dataclasses for records; a
  value that cannot change cannot be changed by mistake.
- **Decide the empty case.** Every method that reads state has an answer for "nothing there yet", and
  the docstring says which.

Next: [Chapter 7 · Modules, contracts and integration](07_modules_and_contracts.md).
