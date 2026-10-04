# Lab 07 solution notes

Two bugs, both at a boundary between modules, both invisible to the unit tests of either module:

1. `ingest.load` returned a dict of columns; `analyse.sensor_means` iterated it and got column *names*.
   The `TypeError` appeared in `analyse`, two calls away from the cause. The contract is now written in
   `ingest.load`'s docstring and tested at the boundary (`test_integration_test_exists_for_the_boundary`).
2. `run.CONFIG` says `thresholds`; `analyse.alerts` read `threshold`. One definition, validated on entry
   with a message that lists the keys actually present.

Who should have caught it: the author of the rewrite (run the pipeline, not just the unit tests), the
reviewer (grep for callers of `load`), and the integration test that did not exist. Now it does.
