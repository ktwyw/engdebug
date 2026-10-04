# Script 3: read a threshold from a config dict (as text, the way a .ini file gives it) and compare.
config = {"high_limit": "120"}
readings = [71.2, 125.4, 70.8]

alerts = [r for r in readings if r > config["high_limit"]]
print(f"{len(alerts)} alert(s): {alerts}")
