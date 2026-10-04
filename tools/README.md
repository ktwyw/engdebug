# Tools

| script | what it does | when to run it |
|---|---|---|
| `make_datasets.py` | writes every file in `datasets/` from a fixed seed | only if you change the generator; the committed files are the course's data |
| `check_labs.py` | runs each lab's tests on the buggy code (must fail) and on the solution (must pass); writes `docs/LAB_STATUS.md` | after editing any lab or solution; CI runs it on every push |

Both are plain scripts: `python tools/check_labs.py`.
