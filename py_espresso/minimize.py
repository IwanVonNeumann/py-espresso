from __future__ import annotations

from dataclasses import dataclass

from py_espresso.cover import Cover
from py_espresso.expand import expand_cover_greedy
from py_espresso.initial import build_initial_cover_greedy
from py_espresso.irredundant import make_irredundant_greedy
from py_espresso.problem import BooleanProblem
from py_espresso.reduce import reduce_cover_greedy


@dataclass(frozen=True, slots=True)
class EspressoGreedyTraceStep:
    iteration: int
    cover: Cover
    reduced: Cover | None = None
    expanded: Cover | None = None
    candidate: Cover | None = None
    accepted: bool = False
    reason: str = ""


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


def minimize_espresso_greedy(
    problem: BooleanProblem,
    max_iter: int = 10,
) -> Cover:
    """
    Iterative Espresso-inspired greedy minimizer.

    This keeps the simple greedy phases as building blocks and accepts only
    reduce-expand-irredundant candidates that improve the cover cost.
    """
    trace = trace_espresso_greedy(problem, max_iter=max_iter)
    return trace[-1].cover


def trace_espresso_greedy(
    problem: BooleanProblem,
    max_iter: int = 10,
) -> list[EspressoGreedyTraceStep]:
    """
    Return the decisions made by the iterative Espresso-inspired minimizer.

    The first trace step has iteration 0 and contains the initial
    greedy+irredundant cover. Later steps contain one
    reduce-expand-irredundant attempt each.
    """
    if max_iter < 0:
        raise ValueError("max_iter must be non-negative")

    cover = build_initial_cover_greedy(problem)
    cover = make_irredundant_greedy(cover, problem)

    if not cover.is_solution(problem):
        raise RuntimeError("minimization produced invalid or incomplete cover")

    trace = [
        EspressoGreedyTraceStep(
            iteration=0,
            cover=cover,
            reason="initial",
        )
    ]

    for iteration in range(1, max_iter + 1):
        reduced = reduce_cover_greedy(cover, problem)
        expanded = expand_cover_greedy(reduced, problem)
        candidate = make_irredundant_greedy(expanded, problem)

        if not candidate.is_solution(problem):
            trace.append(
                EspressoGreedyTraceStep(
                    iteration=iteration,
                    cover=cover,
                    reduced=reduced,
                    expanded=expanded,
                    candidate=candidate,
                    accepted=False,
                    reason="invalid_candidate",
                )
            )
            break

        if candidate.cost() < cover.cost():
            cover = candidate
            trace.append(
                EspressoGreedyTraceStep(
                    iteration=iteration,
                    cover=cover,
                    reduced=reduced,
                    expanded=expanded,
                    candidate=candidate,
                    accepted=True,
                    reason="improved",
                )
            )
        else:
            trace.append(
                EspressoGreedyTraceStep(
                    iteration=iteration,
                    cover=cover,
                    reduced=reduced,
                    expanded=expanded,
                    candidate=candidate,
                    accepted=False,
                    reason="no_improvement",
                )
            )
            break

    return trace
