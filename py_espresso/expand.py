from __future__ import annotations

from py_espresso.cube import Cube
from py_espresso.problem import BooleanProblem


def expand_cube_greedy(
    cube: Cube,
    problem: BooleanProblem,
    *,
    already_covered: set[int] | frozenset[int] | None = None,
) -> Cube:
    """
    Greedily expand a cube while it does not intersect OFF-set.
    """
    if cube.n != problem.n:
        raise ValueError("cube and problem have different dimensions")

    covered = frozenset() if already_covered is None else frozenset(already_covered)

    current = cube

    while True:
        candidates: list[Cube] = []

        for var in current.fixed_variables():
            candidate = current.expand_var(var)

            if problem.cube_is_valid(candidate):
                candidates.append(candidate)

        if not candidates:
            return current

        def score(candidate: Cube) -> tuple[int, int, str]:
            newly_covered_on = problem.on_covered_by(candidate) - covered

            return (
                len(newly_covered_on),
                -candidate.literal_count(),
                _reverse_lex_key(candidate.to_pattern()),
            )

        current = max(candidates, key=score)


def _reverse_lex_key(pattern: str) -> str:
    table = str.maketrans({
        "-": "2",
        "0": "1",
        "1": "0",
    })
    return pattern.translate(table)
