# Error catalog

One minimal example per error class, the usual cause, the fix, and which lab exercises it. Run any
example with `python -c "..."` to see the traceback.

| error | minimal example | usual cause | fix | lab |
|---|---|---|---|---|
| `SyntaxError` | `def f(x) return x` | missing colon, bracket, quote; Python 2 print | the editor's highlighting; run before committing | 01 |
| `IndentationError` | a line indented with a tab after spaces | mixed tabs and spaces | `ruff` / editor set to spaces | 01 |
| `NameError` | `print(valeu)` | typo; variable defined in another scope or after use | linter (F821) | 01 |
| `UnboundLocalError` | assigning to a global inside a function then reading it | shadowing a global | `global`, or better, pass and return | 06 |
| `TypeError` | `71.2 > "120"`, `len(5)`, `f(1, 2)` to a 1-arg function | wrong type, often a string from a file or config | convert at the boundary; type hints + mypy | 01, 11 |
| `AttributeError` | `"abc".uppercase()` | wrong method name; `None` where an object was expected | read the docs; guard against `None` | 01 |
| `KeyError` | `d["sensor"]` when the key is `sensor_id` | wrong key; BOM in a header; renamed config key | `.get` with a default when a default is right; raise with the available keys | 01, 04, 07 |
| `IndexError` | `x[len(x)]` | off-by-one; empty list | iterate with `zip` / `enumerate`; check emptiness | 01, 05 |
| `ValueError` | `float("N/A")`, `datetime.strptime` with the wrong format | data that does not match the expectation | validate, report the row and the value | 03, 04 |
| `ZeroDivisionError` | `sum([]) / len([])` | empty input; a stopped machine (input 0) | a guard with a clear message | 02, 03 |
| `FileNotFoundError` / `PermissionError` | `open("nope.csv")` | wrong path, cwd, permissions | `Path` objects; check `exists()`; raise with the full path | 03 |
| `UnicodeDecodeError` | opening a Latin-1 file as UTF-8 | wrong encoding | know the encoding; `utf-8-sig` for BOM files | 04 |
| `ImportError` / `ModuleNotFoundError` | `import pandas` without pandas | missing dependency; wrong environment; circular import | `pip install -e ".[dev]"`; one venv per project | 11 |
| `RecursionError` | a recursive function without a base case | missing base case; cyclic data | add the base case; iterate instead | - |
| `MemoryError` | `[0] * 10**10`; building a 14 400 x 14 400 matrix for a diagonal | the wrong data structure or algorithm | compute what you need; generators; profile memory | 09 |
| `AssertionError` | `assert window >= 1` | an invariant violated during development | keep asserts for invariants; use explicit checks for user input (asserts are removed by `python -O`) | 06 |
| **logic error** | moving average divides by the window at the start | no traceback: wrong formula, boundary, units, `>=`, float `==` | known-answer tests; property tests | 05 |
| **silent failure** | `except: pass`, `dict.get(k, inf)` | an error was swallowed or defaulted away | specific exceptions; log at WARNING; never return a plausible number for a failure | 03, 08 |
| **state bug** | `def __init__(self, readings=[])` | shared mutable default; class vs instance attribute | `None` default; state in `__init__` (B006) | 06 |
| **integration bug** | one module returns columns, the next expects rows | interface drift between modules | a documented contract and a test at the boundary | 07 |
| **performance bug** | a comprehension over all records inside a loop over records | quadratic work that "runs fine" on the test file | profile; group once; running statistics | 09, 10 |
| **unit error** | viscosity passed in cP to a formula expecting Pa s; Celsius in the ideal gas law; percent for a fraction | no traceback: a number of plausible size, off by 2, 9.8, 100, 273 or 1000 | units in names; SI inside; convert at the boundary; plausibility bounds with "was it given in cP?" | 14 |
| **equation error** | `rho v^2` for `rho v^2 / 2`; `rho Q H` without `g`; `log(dT2/dT1)` for `log(dT1/dT2)` | wrong by a constant factor or a sign; dimensionally wrong | dimensional check on paper; an analytical limit each equation must reproduce | 14 |
| **range-of-validity error** | Blasius at Re = 1000; a water correlation at 150 degC; a table extrapolated | a correlation evaluated where it was never fitted; a meaningless number | every correlation carries its range in the code; refuse the transition regime and extrapolation | 14 |
| **validation error** | a "property" that is a constant; the wrong correlation for the fluid | the equations are solved right and model the wrong thing | reference data with a source in the test; a worked standard example | 14 |
| **environment bug** | tests pass locally, fail in CI | unpinned versions; a file only on your disk; `cwd` assumptions | pin, commit the data, use paths relative to `__file__` | 11 |
