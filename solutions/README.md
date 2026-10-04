# Solutions

One directory per lab with the fixed code and `NOTES.md` explaining each bug, its class, the fix, and
what prevents it; `capstone/` holds the fixed release and a worked postmortem.

`python tools/check_labs.py` runs every lab's tests twice - on the buggy code (must fail) and on the
solution (must pass) - and writes `docs/LAB_STATUS.md`.

Instructors distributing the labs without answers can delete this directory. Learners: open a solution
only after your own tests are green, or after an honest hour of being stuck; then compare, and note what
you would have done differently.
