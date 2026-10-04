# Lab 03 solution notes

Handle or raise? The loader cannot decide what the caller wants to do about a missing file or a bad row,
so it raises - with the path, the row number and the value. `mean_reading` of nothing is a caller's
mistake, so it raises too; returning 0.0 was the silent failure that cost a week.

`raise BadRowError(...) from exc` keeps the original `ValueError` in `__cause__`, so the traceback shows
both the loader's context and Python's reason. `except OSError` names what can go wrong when opening; a
bare `except:` would also catch `KeyboardInterrupt` and `SystemExit`.
