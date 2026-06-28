from __future__ import annotations

from py_espresso.cover import Cover
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


def expand_cover_greedy(
        cover: Cover,
        problem: BooleanProblem,
) -> Cover:
    """
    Expand every cube in an existing cover.

    This is closer to Espresso's EXPAND phase than initial cover building:
    it takes an existing cover and tries to make its cubes larger.
    """
    if not cover.is_valid(problem):
        raise ValueError("cover is not valid: it covers OFF points")

    expanded_cubes: list[Cube] = []
    already_covered: set[int] = set()

    for cube in cover:
        expanded = expand_cube_greedy(
            cube,
            problem,
            already_covered=already_covered,
        )
        expanded_cubes.append(expanded)
        already_covered.update(problem.on_covered_by(expanded))

    return Cover(expanded_cubes).without_duplicates()


def _reverse_lex_key(pattern: str) -> str:
    table = str.maketrans({
        "-": "2",
        "0": "1",
        "1": "0",
    })
    return pattern.translate(table)
