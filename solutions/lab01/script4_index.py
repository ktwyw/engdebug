readings = [71.2, 72.0, 70.8, 73.1]

changes = [b - a for a, b in zip(readings, readings[1:])]  # no index arithmetic, no off-by-one
print([round(c, 10) for c in changes])
