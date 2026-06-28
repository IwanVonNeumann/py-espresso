from __future__ import annotations

from py_espresso.cover import Cover
from py_espresso.expand import expand_cover_greedy
from py_espresso.initial import build_initial_cover_greedy
from py_espresso.irredundant import make_irredundant_greedy
from py_espresso.problem import BooleanProblem
from py_espresso.reduce import reduce_cover_greedy


def minimize_greedy(problem: BooleanProblem) -> Cover:
    cover = build_initial_cover_greedy(problem)
    cover = make_irredundant_greedy(cover, problem)

    if not cover.is_solution(problem):
        raise RuntimeError("minimization produced invalid or incomplete cover")

    return cover


def minimize_greedy_with_reduce(problem: BooleanProblem) -> Cover:
    """
    One reduce-expand-irredundant attempt.

    We only accept the candidate if it improves the cost.
    """
    cover = minimize_greedy(problem)

    reduced = reduce_cover_greedy(cover, problem)
    expanded = expand_cover_greedy(reduced, problem)
    candidate = make_irredundant_greedy(expanded, problem)

    if not candidate.is_solution(problem):
        return cover

    if candidate.cost() < cover.cost():
        return candidate

    return cover
