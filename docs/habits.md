# Good habits, and where the course builds them

Debugging is mostly the absence of certain habits. Each habit below is introduced in a chapter, practised
in a lab, and named in the lab's "Prevent recurrence" section. Together they are the course's real
syllabus.

## Writing code

| habit | why | chapter / lab |
|---|---|---|
| Run early, run often: five lines, then run | errors found in five lines are found in seconds | 1 / 01 |
| Descriptive names, spelled one way, with units (`input_kw`, `limit_kpa`) | most `NameError`s are typos in hasty names; most unit bugs are unlabelled numbers | 1, 5 / 01, 05 |
| Named constants, never literals in formulas (`KPA_PER_BAR = 100.0`) | a literal cannot be searched, explained or changed in one place | 5 / 05 |
| Small functions that do one thing | a function that reads, computes and prints cannot be tested or reused | 2 / 02 |
| Pure functions where possible (inputs in, result out, nothing else touched) | pure functions are trivially testable and cannot have state bugs | 2, 6 / 02, 06 |
| A docstring that states what is returned and what is raised | the contract a test and a caller can be written from | 7 / 07 |
| Type hints on every signature | documentation a tool can check | 10 / 11 |
| `None` as the default for mutable arguments; state in `__init__` | the mutable-default and class-attribute traps | 6 / 06 |
| Prefer immutable data (tuples, frozen dataclasses) | what cannot change cannot be changed by mistake | 6 / 06 |
| Decide the empty case and document it | `IndexError` on an empty list is a class failing to own its boundary | 6 / 06 |

## Handling errors and data

| habit | why | chapter / lab |
|---|---|---|
| Fail loudly: raise, never return a plausible number for a failure | a wrong answer is worse than no answer | 3 / 03 |
| Catch what you name; every `except` has a type and a visible consequence | `except: pass` is the most expensive line in a code base | 3 / 03, 08 |
| Context in every message: what, where, which value | a message you can act on at 3 a.m. | 3 / 03, 04 |
| Assertions for invariants, exceptions for input | `python -O` removes asserts; data validation must survive | 3 / 03 |
| Convert at the boundary, once | text from files and configs becomes numbers in one function | 1, 4 / 01, 04 |
| Encoding and newline always explicit | the default depends on the machine | 4 / 04 |
| Write the input contract first; validate at the boundary, trust inside | validation scattered through the code is validation missing somewhere | 4 / 04 |
| Report every skipped row; never repair silently | silence is the bug | 4 / 04 |
| Keep every file that ever broke the parser, with a test | your test data is the history of what the world sent you | 4 / 04 |
| Configuration defined once, validated on load, read once | config drift and `KeyError`s on other machines | 7, 11 / 07, 13 |

## Engineering correctness

| habit | why | chapter / lab |
|---|---|---|
| Units in every name; SI inside; one conversion function with sourced factors | a parameter called `temperature` invites any unit | 13 / 14 |
| Units written next to every number in a hand calculation, before coding | dimensional homogeneity catches most equation errors on paper | 13 / 14 |
| An analytical benchmark for every equation (a limit, an identity, a scaling law) | a known answer that needs no experiment and that a wrong factor cannot reproduce | 13 / 14 |
| Every correlation carries its range in the code; refuse, do not invent | outside its range a correlation is meaningless, and the code cannot tell | 13 / 14 |
| A benchmark names its source outside the code | otherwise it is a regression test, which catches change, not error | 13 / 14 |
| Verification (right equations, solved right) before validation (right equations for reality), and both recorded | the V&V record is what a reviewer asks for first | 13 / 14 |

## Testing

| habit | why | chapter / lab |
|---|---|---|
| Three tests per function: normal, boundary, error | boundaries are where bugs live | 2 / 02 |
| Known-answer inputs you can compute by hand | the only instrument that detects a wrong formula | 5 / 05 |
| `isclose`/`approx`, never `==`, on floats | `0.1 + 0.2 != 0.3` | 5 / 05 |
| A failing test for every bug, in the same commit as the fix | the test is the bug's gravestone | 2, 10 / all |
| One integration test per module boundary, on real data | unit tests are blind to boundaries | 7 / 07 |
| Tests named for the behaviour, arrange-act-assert, no logic | when it fails, the name is the bug report | 2 / 02 |
| A performance test with a generous bound | a 100x regression should fail CI, not surprise the night shift | 9 / 10 |
| Run the suite before every commit | seconds of insurance | 2 / all |

## Observing and measuring

| habit | why | chapter / lab |
|---|---|---|
| `logging`, never `print`, in library code; configure once in `main` | you can turn it on in production and off in tests | 8 / 08 |
| A count per stage at INFO; a WARNING for every skip, default and ignored error | "it did nothing" becomes diagnosable in ten seconds | 8 / 08 |
| Read the log before reading the code | the program describes itself | 8 / 08 |
| Time it before you touch it, at two sizes | the ratio reveals the complexity | 9 / 09 |
| Profile, then fix the top entry | the slowest line is rarely the ugliest | 9 / 09 |
| The old version is the oracle; equivalence test before speed-up | an optimisation that changes output is a bug | 9 / 10 |

## Working

| habit | why | chapter / lab |
|---|---|---|
| Reproduce before you change; write the command down | a bug you cannot trigger is a bug you cannot know you fixed | 0, 1 / all |
| Write down what you observe before forming a theory | debugging on paper survives interruptions | 0 / all |
| One virtual environment per project; every import declared | "works on my machine" | 0, 11 / 13 |
| Paths from `__file__` or from arguments, never from the working directory | the user's folder is not your folder | 11 / 13 |
| Commit small, with a message that says why | six months later the message is all you have | 10 / 11 |
| Linter and type checker in the editor and in CI; never silence a tool without a written reason | errors without running | 10 / 11 |
| "What changed?" before "what is wrong?" | the diff is the first diagnostic | 12 / capstone |
| Bug reports with symptom, reproduction, expected, environment | half of debugging is communication | 12 / capstone |
| Blameless postmortems with the detection gap as the longest section | what let it through is what to fix | 12 / capstone |
