# py-espresso

`py-espresso` is a Python project for heuristic minimization of Boolean
functions.

The current implementation is **Espresso-inspired**, but it is not yet a
canonical Berkeley Espresso implementation. The project is being developed
incrementally: simple greedy baselines are kept for comparison, while the
algorithmic phases are gradually moved toward a more complete and trustworthy
Espresso-style minimizer.

## Current model

- Single-output Boolean functions.
- Input as `ON` and `DC` sets; `OFF` is derived from the remaining minterms.
- Cubes represented by bit masks: `value`, `care`, and `n`.
- Covers represented as immutable-style collections of cubes.

## Implemented algorithms

- `minimize_greedy(problem)`
- `minimize_greedy_with_reduce(problem)`
- `minimize_espresso_greedy(problem, max_iter=10)`
- `trace_espresso_greedy(problem, max_iter=10)`

The default cover cost is `(cube_count, literal_count)`, where smaller tuples
are better.

## Development status

This is an early research/prototyping implementation. The code prioritizes
clarity, tests, and traceability before low-level performance tuning.

See `docs/algorithm_notes.md` for the current algorithm notes, limitations,
and the relationship to Espresso.
