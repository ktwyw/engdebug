# Debugger walkthrough: `pdb`, `breakpoint()` and the IDE

Printing is a debugger with no undo. The real thing lets you stop a running program, look at every
variable in every frame, and step one line at a time. Twenty minutes with it pays back in the first week.

## Stop at the crash (post-mortem)

```bash
python -m pdb labs/lab07_integration/buggy/run.py datasets/clean/sensor_day2.csv
(Pdb) c                      # continue until the exception
(Pdb) bt                     # the call stack: where am I, and who called me
(Pdb) p type(records)        # the variable the crashing line used -> <class 'dict'>
(Pdb) u                      # go UP one frame, into main()
(Pdb) p records.keys()       # dict_keys(['timestamp', 'sensor_id', 'reading', 'unit']): the cause
(Pdb) q
```

The error was raised in `analyse.alerts`; the cause lived one frame up. `u`/`d` move between frames;
`p` prints; `pp` pretty-prints; `l` lists the source around the current line.

## Stop before the crash (a breakpoint)

Put `breakpoint()` on any line (Python 3.7+; it opens `pdb`) and run normally:

```python
def alerts(records, config):
    breakpoint()           # execution pauses here
    out = []
    for rec in records:
```

```
(Pdb) n        # next line (step OVER calls)
(Pdb) s        # step INTO the call on this line
(Pdb) p rec    # inspect
(Pdb) c        # continue to the next breakpoint or the end
(Pdb) b 19     # set a breakpoint at line 19; "b" alone lists them; "cl 1" clears the first
(Pdb) until 25 # run until line 25
(Pdb) w        # where (same as bt)
```

Conditional breakpoint: `b analyse.py:19, rec["unit"] == "degC"` stops only for that case - the way to
catch "it only happens on some rows" (lab 08) without stepping through 1 700 of them.

## In pytest

`python -m pytest labs/lab07_integration -x --pdb` drops into the debugger at the first failing
assertion with the test's variables in scope. `--trace` stops at the start of each test.

## In the IDE

VS Code: click left of a line number to set a breakpoint, press F5 (Run and Debug, "Python File"); the
*Variables* pane is `p` for everything, *Call Stack* is `bt`, *Watch* re-evaluates an expression every
step, and the *Debug Console* is a `pdb` prompt with autocompletion. For pytest, install the Python
extension's Testing panel and use "Debug Test" on a test name. PyCharm: the same with Shift+F9.

## When to use which

- a traceback you do not understand: post-mortem `pdb`, `bt`, then `u` until the variables make sense;
- a wrong value with no crash: a breakpoint just before the value is used, then `n` and `p`;
- a rare case: a conditional breakpoint;
- something that only happens in the loop's 1 400th iteration: `until`, or log it (lab 08) and read.

The debugger finds *where*; the test you write afterwards (lab 02) keeps it found.
