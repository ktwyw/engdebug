# Lab 02 solution notes

- `efficiency`: the formula was inverted (`input / output`); and a stopped machine (input 0) divided by
  zero, a sensor fault (output > input) produced 125 %. Guards with messages that carry the values.
- `capacity_factor`: `energy / rated * hours` is `(energy / rated) * hours`; the denominator needs
  parentheses. The test with 2400 kWh at 100 kW over 24 h (exactly 1.0) exposes it immediately.
- `specific_energy`: correct, but a zero volume gave `ZeroDivisionError` with no context.

Three kinds of test per function: normal (0.8), boundary (1.0), error (`pytest.raises`).
