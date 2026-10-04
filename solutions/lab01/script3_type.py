config = {"high_limit": "120"}
readings = [71.2, 125.4, 70.8]

high_limit = float(config["high_limit"])  # convert at the boundary: config files hold strings
alerts = [r for r in readings if r > high_limit]
print(f"{len(alerts)} alert(s): {alerts}")
