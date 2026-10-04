"""Chapter 9: a quadratic loop, its linear fix, the scaling test and a profile.
Run:  python examples/ch09_profile.py
      python -m cProfile -s tottime examples/ch09_profile.py | head -20"""

import time


def group_quadratic(records):
    """Looks harmless: for each record, collect all records with the same id."""
    groups = {}
    for rec in records:
        groups[rec["id"]] = [r for r in records if r["id"] == rec["id"]]  # scans everything, every time
    return groups


def group_linear(records):
    groups = {}
    for rec in records:
        groups.setdefault(rec["id"], []).append(rec)  # one pass
    return groups


def timed(fn, *args):
    t0 = time.perf_counter()
    out = fn(*args)
    return out, time.perf_counter() - t0


if __name__ == "__main__":
    for n in (2_000, 20_000):
        records = [{"id": f"S{i % 6}", "value": float(i)} for i in range(n)]
        (gq, tq), (gl, tl) = timed(group_quadratic, records), timed(group_linear, records)
        assert gq == gl, "the two must agree exactly"
        print(f"n = {n:>6}: quadratic {tq:7.3f} s   linear {tl:7.4f} s")
    print("10x the data: the quadratic version takes ~100x longer, the linear ~10x")
