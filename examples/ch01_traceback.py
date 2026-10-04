"""Chapter 1: a traceback whose cause is two frames above where it is raised.
Run:  python examples/ch01_traceback.py        (it crashes on purpose; read the traceback bottom-up, then top-down)
Then: python -m pdb examples/ch01_traceback.py  and type  c, bt, u, p config  to walk the frames."""


def load_config():
    # the cause: the key is misspelled HERE ...
    return {"treshold": {"degC": 120.0}}


def alerts(records, config):
    # ... but Python only notices HERE, two calls later
    limit = config["threshold"]["degC"]
    return [r for r in records if r > limit]


def main():
    config = load_config()
    readings = [71.2, 125.4, 70.8]
    print(alerts(readings, config))


if __name__ == "__main__":
    main()
