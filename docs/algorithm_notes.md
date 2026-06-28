# Algorithm Notes

This document records what the current minimizer does, how it relates to
Espresso, and which limitations are still open. It is intentionally conservative:
the implementation should not be presented as canonical Espresso until the
missing pieces are understood and implemented or explicitly justified.

## Current Goal

The project currently builds a clear, testable Boolean function minimizer that
uses Espresso-like ideas. This minimizer is intended as a reliable component for
larger work, not as the final research contribution by itself.

## Problem Model

- A problem is represented as `BooleanProblem(n, on, dc)`.
- `ON` contains minterms that must be covered.
- `DC` contains don't-care minterms that may be covered.
- `OFF` is derived as all minterms not in `ON` or `DC`; it must not be covered.
- The first implementation targets single-output functions.
- Multi-output minimization is a future extension.

## Data Model

- A cube is represented as `Cube(value, care, n)`.
- `care` marks fixed variables.
- A zero bit in `care` means the variable is free inside the cube.
- Pattern strings such as `"01--1"` are used only for tests, traces, and
  debugging.
- A cover is a tuple-like collection of cubes.

## Implemented Phases

### Initial Cover

`build_initial_cover_greedy(problem)` starts from uncovered ON minterms and
expands each minterm greedily while avoiding OFF.

This is a constructor for a valid starting cover, not a full Espresso phase.

### Expand

`expand_cube_greedy(cube, problem, already_covered=None)` greedily removes fixed
variables when the resulting cube does not intersect OFF.

`expand_cover_greedy(cover, problem)` applies this logic to each cube in a cover.

This captures the broad idea of Espresso's EXPAND phase, but the current
heuristic is much simpler than canonical Espresso.

### Irredundant

`make_irredundant_greedy(cover, problem)` repeatedly removes cubes whose removal
still leaves the whole ON-set covered.

This implements a simple greedy irredundancy pass.

### Reduce

`reduce_cover_greedy(cover, problem)` keeps, for each cube, the ON points covered
uniquely by that cube and replaces the cube by the most general subcube that
still covers those unique points.

This is an intentionally simple REDUCE-style operation. It may worsen cost by
itself, so minimizers should not return directly after REDUCE.

## Implemented Minimizers

### `minimize_greedy(problem)`

Builds an initial greedy cover and makes it irredundant.

### `minimize_greedy_with_reduce(problem)`

Runs one reduce-expand-irredundant attempt and accepts the candidate only if its
cost improves.

### `minimize_espresso_greedy(problem, max_iter=10)`

Runs iterative reduce-expand-irredundant attempts and accepts only candidates
that improve cost.

This is currently the closest function to an Espresso-style loop, but it is
still an Espresso-inspired greedy minimizer rather than canonical Espresso.

### `trace_espresso_greedy(problem, max_iter=10)`

Returns the sequence of decisions made by `minimize_espresso_greedy`.

The first step records the initial greedy+irredundant cover. Later steps record
the reduced cover, expanded cover, irredundant candidate, acceptance decision,
and current accepted cover.

## Tested Properties

Current tests check that:

- `Cube` operations preserve the intended bit-mask semantics.
- The 5-variable example is minimized by the greedy baseline to cost `(2, 5)`.
- The Espresso-inspired greedy minimizer returns a valid complete solution not
  worse than the greedy baseline on the 5-variable example.
- `reduce_cover_greedy` preserves a valid complete solution.
- `expand_cover_greedy` preserves validity.
- `make_irredundant_greedy` preserves a solution and removes an explicitly
  redundant cube.
- `minimize_espresso_greedy(problem, max_iter=0)` matches the greedy baseline.
- `trace_espresso_greedy` starts with a valid initial solution, accepted steps
  improve cost, and its final cover matches `minimize_espresso_greedy`.

## Known Limitations

- Many operations enumerate `range(1 << n)`, which is not suitable for genuinely
  large `n`.
- OFF is derived by full enumeration, so sparse or symbolic representations will
  be needed later.
- The current implementation is single-output only.
- The current EXPAND, REDUCE, and IRREDUNDANT phases are simplified greedy
  versions.
- No claim is currently made that this is equivalent to Berkeley Espresso.

## Near-Term Direction

- Add more examples, including cases where reduce-expand-irredundant improves a
  greedy baseline.
- Compare behavior against a trusted reference implementation or documented
  Espresso examples.
- Gradually replace simplified greedy choices with more faithful or better
  justified heuristics.
