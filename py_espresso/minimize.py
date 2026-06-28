from __future__ import annotations

from py_espresso.cover import Cover
from py_espresso.expand import expand_cover_greedy
from py_espresso.irredundant import make_irredundant_greedy
from py_espresso.problem import BooleanProblem


def minimize_greedy(problem: BooleanProblem) -> Cover:
    """
    First working minimizer.

    Pipeline:
        1. Build a greedy expanded cover.
        2. Remove redundant cubes.

    This is not full Espresso yet, because it has no reduce/iterate phase.
    """
    cover = expand_cover_greedy(problem)
    cover = make_irredundant_greedy(cover, problem)

    if not cover.is_solution(problem):
        raise RuntimeError("minimization produced invalid or incomplete cover")

    return cover
