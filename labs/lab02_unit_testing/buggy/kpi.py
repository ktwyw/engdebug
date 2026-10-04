"""Key performance indicators for a pump. The operators say the efficiency numbers "look wrong"."""


def efficiency(output_kw, input_kw):
    """Efficiency of a machine as a fraction in [0, 1]."""
    return input_kw / output_kw


def capacity_factor(energy_kwh, rated_kw, hours):
    """Fraction of the rated energy actually delivered over a period."""
    return energy_kwh / rated_kw * hours


def specific_energy(energy_kwh, volume_m3):
    """Energy per cubic metre pumped, kWh/m3."""
    return energy_kwh / volume_m3
