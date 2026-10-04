record = {"sensor_id": "T101", "reading": 71.2, "unit": "degC"}

sensor = record["sensor_id"]  # KeyError: the key is 'sensor_id'
label = record["unit"].upper()  # AttributeError: str has upper(), not uppercase()
print(f"{sensor}: {record['reading']} {label}")
