from __future__ import annotations

from py_espresso.cube import Cube
from py_espresso.problem import BooleanProblem


def expand_candidates(
        cube: Cube,
        problem: BooleanProblem,
) -> list[Cube]:
    """All valid one-variable expansions of a cube."""
    candidates: list[Cube] = []

    for index in cube.fixed_variables():
        candidate = cube.expand_var(index)

        if problem.cube_is_valid(candidate):
            candidates.append(candidate)

    return candidates


def expand_cube_greedy(
        cube: Cube,
        problem: BooleanProblem,
) -> Cube:
    """
    Greedily expand cube while it can be expanded without covering OFF.

    Current simple heuristic:
        choose candidate with the fewest literals;
        if tied, choose one covering more ON points;
        if tied, choose lexicographically by pattern for determinism.
    """
    current = cube

    while True:
        candidates = expand_candidates(current, problem)

        if not candidates:
            return current

        current = min(
            candidates,
            key=lambda c: (
                c.literal_count(),
                -len(problem.on_covered_by(c)),
                c.to_pattern(),
            ),
        )
