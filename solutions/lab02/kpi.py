"""Key performance indicators for a pump (fixed)."""


def efficiency(output_kw, input_kw):
    """Efficiency of a machine as a fraction in [0, 1]."""
    if input_kw <= 0:
        raise ValueError(f"input power must be positive, got {input_kw}")
    if output_kw < 0:
        raise ValueError(f"output power cannot be negative, got {output_kw}")
    if output_kw > input_kw:
        raise ValueError(f"output {output_kw} exceeds input {input_kw}: check the sensors")
    return output_kw / input_kw  # was input / output


def capacity_factor(energy_kwh, rated_kw, hours):
    """Fraction of the rated energy actually delivered over a period."""
    if rated_kw <= 0 or hours <= 0:
        raise ValueError(f"rated power and hours must be positive, got {rated_kw} kW, {hours} h")
    return energy_kwh / (rated_kw * hours)  # was energy / rated * hours (precedence)


def specific_energy(energy_kwh, volume_m3):
    """Energy per cubic metre pumped, kWh/m3."""
    if volume_m3 <= 0:
        raise ValueError(f"volume must be positive, got {volume_m3}")
    return energy_kwh / volume_m3
