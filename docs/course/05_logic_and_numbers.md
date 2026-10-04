# Chapter 5 · Logic and numbers: the bugs with no traceback

*For lab 05. Runnable example: `examples/ch05_floats.py`.*

## The hardest bugs are quiet

A `KeyError` announces itself. A moving average that is 30 % too low at the start of every series does
not: it produces plausible numbers, the dashboard shows them, and engineering decisions are made on them
for two months. Logic bugs - wrong formulas, wrong boundaries, wrong operators, wrong units - have no
traceback. The only instrument that detects them is a **known-answer test**: an input whose correct output
you know independently of the code.

## Floating-point numbers

Computers store real numbers in binary with about 16 significant decimal digits. Most decimal fractions
have no exact binary representation, so `0.1` is stored as the nearest representable number, which is
not quite 0.1. The consequences:

```python
>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3
False
>>> sum([0.1] * 10) == 1.0
False
```

Rules:

- **Never compare floats with `==`.** Use `math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)` in code and
  `pytest.approx` in tests. `rel_tol` is a fraction of the magnitude; `abs_tol` matters when the expected
  value is zero (a relative tolerance of zero is zero).
- **Order of operations changes the last digits.** `(a + b) + c` and `a + (b + c)` can differ in the
  16th digit; a running sum and a fresh sum differ too. When you optimise (chapter 9) compare with a
  tolerance, not exactly.
- **Subtracting nearly equal numbers loses precision.** `(Q - S*mu)/(m-1)` for a variance can come out
  as `-1e-15` for a constant series; clamp at zero before `sqrt`.
- **Integers are exact.** Count in integers, convert to float at the end. Money and anything that must
  add up exactly uses `decimal.Decimal` or integer cents.
- **Printing rounds.** `print(0.1 + 0.2)` shows `0.30000000000000004` but `f"{x:.2f}"` shows `0.30`; a
  value that *looks* right in a report may not be the value that was compared.

## Boundaries and off-by-one

Almost every loop has an edge where the usual rule does not apply, and that edge is where the bug is:

- `range(len(x))` with `x[i + 1]` inside: the last iteration reads past the end. Iterate over
  `zip(x, x[1:])` or `range(len(x) - 1)`, and write the test for the last element.
- `range(1, n)` when you meant every element: the first is skipped; a sum over it is short by one
  term (lab 05's `drift`).
- a trailing window at the start of a series has fewer than `window` values; dividing by `window`
  instead of by the number of values present biases the first points towards zero. Divide by what you
  actually summed.
- `<` or `<=`? `lo <= x <= hi` for an inclusive range; decide, write it in the docstring, test the
  value exactly on the boundary. The *strictly above* count uses `>`; `>=` counts the threshold itself.
- fence posts: ten readings five minutes apart span 45 minutes, not 50.

The known-answer inputs for boundaries: an empty list, one element, two elements, `window` equal to the
length, the value exactly on the limit.

## Units

A number without a unit is a bug waiting to be interpreted. `pressure_ok(13, "bar")` passing a 1200 kPa
limit because the unit argument was accepted and ignored is lab 05's most expensive bug, and the
industry has lost spacecraft to the same class. Rules:

- put the unit in the name: `limit_kpa`, `time_s`, `input_kw`;
- convert at the boundary to one internal unit per quantity and never mix inside;
- when a function accepts a unit argument, it must either convert or raise for a unit it does not know;
  silently proceeding is not an option;
- a conversion is a named constant (`KPA_PER_BAR = 100.0`), not a literal in the middle of a formula.

## Formulas

`sum(x) ** 2` and `sum(v ** 2 for v in x)` are one keystroke apart and differ by a factor of n for a
constant series. `energy / rated * hours` is `(energy / rated) * hours`. `input / output` is the inverse
of what efficiency means. None of these raise. All of them are caught by one test with an input whose
answer you know: `rms([3, 4])` is `sqrt(12.5)`; a capacity factor of a machine at full load for the whole
period is exactly 1; the efficiency of 80 from 100 is 0.8.

Write the formula on paper first, with units; then write the test from the paper; then the code.

## Thinking in invariants

An invariant is something that must be true regardless of the data: a mean lies between the minimum and
the maximum; a standard deviation is not negative; efficiency is in [0, 1]; a count is an integer; a
moving average of a constant series is that constant; converting a unit and back is the identity. Each
is a test you can write without knowing any particular answer, and `hypothesis` can throw a thousand
random inputs at it (chapter 2). When a known answer is hard to construct, an invariant is often easy.

## A method for a wrong number

1. Find the smallest input that produces a wrong result (two values, a window of 2).
2. Compute the right answer by hand. Write it down.
3. Add `print` statements for each intermediate quantity, or step through with the debugger (chapter 10),
   and find the first intermediate value that differs from your hand calculation. The bug is on the line
   that produced it.
4. Fix; turn your hand calculation into a test.

## Habits this chapter starts

- **Known answers first.** Before trusting any formula, one input you can compute by hand, in a test.
- **Units in names, constants with names.** `KPA_PER_BAR`, `limit_kpa`; no bare `100.0` in a formula.
- **`isclose`, never `==`, on floats.** In code and in tests.
- **Test the edges.** Empty, one, two, exactly on the limit, the last element.
- **Docstrings state the contract.** "Trailing moving average over the last `window` values (fewer at
  the start)" is a sentence a test can be written from; "computes the average" is not.

Next: [Chapter 6 · Classes and state](06_classes_and_state.md).
