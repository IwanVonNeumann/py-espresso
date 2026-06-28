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

    Educational heuristic:
        among all valid one-variable expansions, choose the candidate
        covering the largest number of not-yet-covered ON points.

    Tie-breaks:
        1. fewer literals
        2. lexicographically smallest pattern
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

        best = max(candidates, key=score)

        current = best


def expand_cover_greedy(problem: BooleanProblem) -> Cover:
    """
    Build a cover greedily from currently uncovered ON minterms.

    Algorithm:
        1. Start with an empty cover.
        2. Pick the smallest uncovered ON minterm.
        3. Make a one-point cube from it.
        4. Expand it greedily.
        5. Add the expanded cube to the cover.
        6. Mark newly covered ON points.
        7. Repeat until all ON points are covered.
    """
    covered_on: set[int] = set()
    cubes: list[Cube] = []

    while covered_on != set(problem.on):
        uncovered = sorted(problem.on - covered_on)
        start_point = uncovered[0]

        start_cube = Cube.from_minterm(start_point, n=problem.n)

        expanded = expand_cube_greedy(
            start_cube,
            problem,
            already_covered=covered_on,
        )

        cubes.append(expanded)
        covered_on.update(problem.on_covered_by(expanded))

    return Cover(cubes).without_duplicates()


def _reverse_lex_key(pattern: str) -> str:
    """
    Helper for deterministic tie-breaking with max(...).

    We want lexicographically smallest pattern to win.
    Since max() chooses the largest tuple, invert characters.
    """
    table = str.maketrans({
        "-": "2",
        "0": "1",
        "1": "0",
    })
    return pattern.translate(table)
