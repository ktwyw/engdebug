"""Load a readings file. When something goes wrong this loader prints a message and carries on, which is
how a whole shift of readings went missing from last Tuesday's report without anyone noticing."""

import csv


def load(path):
    readings = []
    try:
        with open(path) as f:
            for row in csv.DictReader(f):
                try:
                    readings.append(float(row["reading"]))
                except:
                    pass
    except:
        print("could not load file")
    return readings


def mean_reading(path):
    readings = load(path)
    try:
        return sum(readings) / len(readings)
    except:
        return 0.0
