from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from py_espresso.cover import Cover
from py_espresso.cube import Cube
from py_espresso.expand import expand_cube_greedy
from py_espresso.initial import build_initial_cover_greedy
from py_espresso.irredundant import make_irredundant_greedy
from py_espresso.minimize import (
    minimize_espresso_greedy,
    minimize_greedy,
    minimize_greedy_with_reduce,
    trace_espresso_greedy,
)
from py_espresso.problem import BooleanProblem
from py_espresso.reduce import reduce_cover_greedy


def show_cube(problem: BooleanProblem, cube: Cube) -> None:
    print(f"cube: {cube}")
    print(f"points: {sorted(problem.cube_points(cube))}")
    print(f"ON: {sorted(problem.on_covered_by(cube))}")
    print(f"DC: {sorted(problem.dc_covered_by(cube))}")
    print(f"OFF: {sorted(problem.off_covered_by(cube))}")
    print(f"valid: {problem.cube_is_valid(cube)}")
    print()


def show_cover(problem: BooleanProblem, cover: Cover) -> None:
    print("cover:")
    for cube in cover:
        print(f"  {cube}")

    print(f"cube count: {cover.cube_count()}")
    print(f"literal count: {cover.literal_count()}")
    print(f"cost: {cover.cost()}")
    print(f"covered ON: {sorted(cover.covered_on(problem))}")
    print(f"covered DC: {sorted(cover.covered_dc(problem))}")
    print(f"covered OFF: {sorted(cover.covered_off(problem))}")
    print(f"valid: {cover.is_valid(problem)}")
    print(f"complete: {cover.is_complete(problem)}")
    print(f"solution: {cover.is_solution(problem)}")
    print()


def show_espresso_trace(problem: BooleanProblem) -> None:
    for step in trace_espresso_greedy(problem):
        if step.iteration == 0:
            print(f"initial: cost={step.cover.cost()}")
            continue

        print(f"iter {step.iteration}:")
        print(f"  reduced: cost={step.reduced.cost()}")
        print(f"  expanded: cost={step.expanded.cost()}")
        print(f"  candidate: cost={step.candidate.cost()}")
        print(f"  decision: {step.reason}")
        print(f"  current: cost={step.cover.cost()}")


def main() -> None:
    problem = BooleanProblem(
        n=5,
        on={1, 3, 5, 7, 9, 13, 17, 21, 25, 29},
        dc={0, 4, 12, 16, 20, 24, 28},
    )

    print("=" * 60)
    print("Initial cover from ON minterms")
    print("=" * 60)
    print()

    initial_cover = Cover.from_minterms(sorted(problem.on), n=problem.n)
    show_cover(problem, initial_cover)

    print("=" * 60)
    print("Manual expansion of one cube")
    print("=" * 60)
    print()

    cube = Cube.from_minterm(5, n=5)
    show_cube(problem, cube)

    cube = cube.expand_var(0)
    show_cube(problem, cube)

    cube = cube.expand_var(1)
    show_cube(problem, cube)

    for candidate in [
        cube.expand_var(2),  # ---01
        cube.expand_var(3),  # --1-1
        cube.expand_var(4),  # --10-
    ]:
        show_cube(problem, candidate)

    print("=" * 60)
    print("Greedy expansion of one cube")
    print("=" * 60)
    print()

    start = Cube.from_minterm(5, n=5)
    expanded = expand_cube_greedy(start, problem)
    show_cube(problem, expanded)

    print("=" * 60)
    print("First hand-built cover")
    print("=" * 60)
    print()

    hand_cover = Cover(
        [
            Cube.from_pattern("---01"),
            Cube.from_pattern("00-11"),
        ]
    )
    show_cover(problem, hand_cover)

    print("=" * 60)
    print("Initial greedy cover")
    print("=" * 60)
    print()

    greedy_cover = build_initial_cover_greedy(problem)
    show_cover(problem, greedy_cover)

    print("=" * 60)
    print("Irredundant greedy cover")
    print("=" * 60)
    print()

    irredundant_cover = make_irredundant_greedy(greedy_cover, problem)
    show_cover(problem, irredundant_cover)

    print("=" * 60)
    print("Reduced cover")
    print("=" * 60)
    print()

    reduced_cover = reduce_cover_greedy(irredundant_cover, problem)
    show_cover(problem, reduced_cover)

    print("=" * 60)
    print("Minimize greedy")
    print("=" * 60)
    print()

    solution = minimize_greedy(problem)
    show_cover(problem, solution)

    print("=" * 60)
    print("Minimize greedy with reduce")
    print("=" * 60)
    print()

    reduced_solution = minimize_greedy_with_reduce(problem)
    show_cover(problem, reduced_solution)

    print("=" * 60)
    print("Minimize Espresso-inspired greedy")
    print("=" * 60)
    print()

    espresso_solution = minimize_espresso_greedy(problem)
    show_cover(problem, espresso_solution)

    print("=" * 60)
    print("Espresso-inspired greedy trace")
    print("=" * 60)
    print()

    show_espresso_trace(problem)


if __name__ == "__main__":
    main()
