from __future__ import annotations

from py_espresso.cover import Cover
from py_espresso.initial import build_initial_cover_greedy
from py_espresso.irredundant import make_irredundant_greedy
from py_espresso.problem import BooleanProblem


def minimize_greedy(problem: BooleanProblem) -> Cover:
    """
    First working minimizer.

    Pipeline:
        1. Build an initial greedy cover.
        2. Remove redundant cubes.
    """
    cover = build_initial_cover_greedy(problem)
    cover = make_irredundant_greedy(cover, problem)

    if not cover.is_solution(problem):
        raise RuntimeError("minimization produced invalid or incomplete cover")

    return cover
