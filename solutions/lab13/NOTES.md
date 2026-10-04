# Lab 13 solution notes

| failure | environment difference | assumption in the code | fix |
|---|---|---|---|
| `ModuleNotFoundError: yaml` | PyYAML installed on the laptop, not in CI | "my packages are everyone's packages" | standard-library `json`; or a guarded optional import; never an undeclared dependency |
| `FileNotFoundError: datasets/...` | started from a different directory | "the working directory is the repository root" | a path relative to `__file__` (or passed in) |
| `KeyError: 'PRESSURE_TOLERANCE'`, then `TypeError` | variable unset; or set, but a string | "the variable exists and is a number" | `os.environ.get` with a default, `float()` at the boundary, a `ValueError` naming the variable |

The solution's `parents[2]` differs from the lab's `parents[3]` because the solution file sits one level
higher (`solutions/lab13/` against `labs/lab13_environment/buggy/`); computing the root from `__file__`
is right in both places, which is the point.
