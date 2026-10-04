# Lab 01 solution notes

| script | error | cause | fix |
|---|---|---|---|
| 1 | SyntaxError | missing `:` after `def mean(values)` | add the colon |
| 2 | NameError | `valeu` typo | `value` |
| 3 | TypeError | `float > str`: config values are strings | `float(config["high_limit"])` at the boundary |
| 4 | IndexError | `readings[i + 1]` on the last index | iterate `zip(readings, readings[1:])` |
| 5 | KeyError, then AttributeError | key is `sensor_id`; method is `upper` | fix both |

Script 4's printed values are rounded to avoid `0.7999999999999972`: floating-point subtraction is exact
only for representable numbers; the test tolerates the noise either way.
