# Script 1: compute the mean temperature of a shift. It does not even start.
readings = [71.2, 72.0, 70.8, 73.1]

def mean(values)
    return sum(values) / len(values)

print(f"mean temperature: {mean(readings):.2f} degC")
