# Script 5: summarise a record. Two different errors hide here; fix both.
record = {"sensor_id": "T101", "reading": 71.2, "unit": "degC"}

sensor = record["sensor"]
label = record["unit"].uppercase()
print(f"{sensor}: {record['reading']} {label}")
