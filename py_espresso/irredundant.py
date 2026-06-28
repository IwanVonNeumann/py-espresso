from __future__ import annotations

from py_espresso.cover import Cover
from py_espresso.problem import BooleanProblem


def make_irredundant_greedy(
        cover: Cover,
        problem: BooleanProblem,
) -> Cover:
    """
    Greedily remove redundant cubes from a cover.

    A cube is redundant if removing it still leaves all ON points covered.

    This is a simple first version:
        scan cubes from left to right;
        remove a cube whenever it is safe to remove it;
        repeat until no more cubes can be removed.
    """
    if not cover.is_valid(problem):
        raise ValueError("cover is not valid: it covers OFF points")

    current = cover.without_duplicates()

    changed = True
    while changed:
        changed = False

        for index in range(len(current)):
            candidate = current.remove_at(index)

            if candidate.is_complete(problem):
                current = candidate
                changed = True
                break

    return current
