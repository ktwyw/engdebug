"""Chapter 2: a function and its three tests in one file.
Run:  python -m pytest examples/ch02_first_test.py -q
Then break efficiency() on purpose (swap the division) and run again to see what a failure looks like."""

import pytest


def efficiency(output_kw: float, input_kw: float) -> float:
    """Useful output over input, as a fraction in [0, 1]."""
    if input_kw <= 0:
        raise ValueError(f"input power must be positive, got {input_kw}")
    if output_kw > input_kw:
        raise ValueError(f"output {output_kw} exceeds input {input_kw}: check the sensors")
    return output_kw / input_kw


def test_normal_case():
    assert efficiency(80.0, 100.0) == pytest.approx(0.8)


def test_boundary_equal_powers():
    assert efficiency(100.0, 100.0) == 1.0


@pytest.mark.parametrize("inp", [0.0, -5.0])
def test_error_case_non_positive_input(inp):
    with pytest.raises(ValueError, match="input power must be positive"):
        efficiency(50.0, inp)
