pressures_bar = [6.1, 6.3, 5.9]


def to_kpa(value):
    return value * 100.0  # 'valeu' was a typo: NameError


print([to_kpa(p) for p in pressures_bar])
