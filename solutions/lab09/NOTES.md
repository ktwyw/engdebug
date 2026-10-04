# Lab 09 solution notes

The deliverable is `hotspots.md` (the profile and the ranked hotspots) and the `timed` helper added to
`slow.py`. No optimisation is made in this lab on purpose: lab 10's speed-up must be measured against
this baseline, and the discipline of *measuring before changing* is the whole lesson. The surprise most
students report: the line they would have optimised first (`report += ...`) is 0.1 % of the time, and
the one that owns 93 % looks like ordinary, tidy Python.
