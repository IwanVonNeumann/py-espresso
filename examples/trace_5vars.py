from py_espresso.cover import Cover
from py_espresso.cube import Cube
from py_espresso.expand import expand_cube_greedy
from py_espresso.problem import BooleanProblem


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


if __name__ == "__main__":
    main()
