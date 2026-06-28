from __future__ import annotations

from py_espresso.cover import Cover
from py_espresso.cube import Cube
from py_espresso.problem import BooleanProblem


def reduce_cover_greedy(
    cover: Cover,
    problem: BooleanProblem,
) -> Cover:
    """
    Simple REDUCE phase.

    For each cube, keep only the ON points that are covered uniquely by
    this cube. Then replace the cube by the most general subcube that still
    covers those unique points.

    This preserves completeness.
    """
    if not cover.is_solution(problem):
        raise ValueError("reduce expects a valid complete cover")

    reduced_cubes: list[Cube] = []

    for index, cube in enumerate(cover):
        other_cover = cover.remove_at(index)

        uniquely_covered_on = (
            problem.on_covered_by(cube)
            - other_cover.covered_on(problem)
        )

        if not uniquely_covered_on:
            # This cube is redundant; irredundant phase may remove it.
            reduced_cubes.append(cube)
            continue

        reduced = _smallest_subcube_covering_points(
            cube=cube,
            points=uniquely_covered_on,
        )

        reduced_cubes.append(reduced)

    return Cover(reduced_cubes)


def _smallest_subcube_covering_points(
    cube: Cube,
    points: frozenset[int],
) -> Cube:
    """
    Return the most general cube contained in `cube` that covers all points.

    Since the result is contained in the original cube, it cannot cover OFF
    if the original cube was valid.
    """
    if not points:
        raise ValueError("points must not be empty")

    value = cube.value
    care = cube.care

    for var in cube.free_variables():
        bit = cube.n - 1 - var
        mask = 1 << bit

        values = {(point & mask) != 0 for point in points}

        if len(values) == 1:
            # All required points agree on this variable,
            # so we may fix it.
            care |= mask

            if True in values:
                value |= mask
            else:
                value &= ~mask

    return Cube(value=value, care=care, n=cube.n)
