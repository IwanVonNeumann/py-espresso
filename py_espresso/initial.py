from __future__ import annotations

from py_espresso.cover import Cover
from py_espresso.cube import Cube
from py_espresso.expand import expand_cube_greedy
from py_espresso.problem import BooleanProblem


def build_initial_cover_greedy(problem: BooleanProblem) -> Cover:
    """
    Build an initial cover greedily from uncovered ON minterms.

    This is not the full Espresso EXPAND phase.
    It is just a constructor for the first valid cover.
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
