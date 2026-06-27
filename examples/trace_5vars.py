from py_espresso.cube import Cube
from py_espresso.problem import BooleanProblem


def show_cube(problem: BooleanProblem, cube: Cube) -> None:
    print(f"cube: {cube}")
    print(f"points: {sorted(problem.cube_points(cube))}")
    print(f"ON: {sorted(problem.on_covered_by(cube))}")
    print(f"DC: {sorted(problem.dc_covered_by(cube))}")
    print(f"OFF: {sorted(problem.off_covered_by(cube))}")
    print(f"valid: {problem.cube_is_valid(cube)}")
    print()


def main() -> None:
    problem = BooleanProblem(
        n=5,
        on={1, 3, 5, 7, 9, 13, 17, 21, 25, 29},
        dc={0, 4, 12, 16, 20, 24, 28},
    )

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


if __name__ == "__main__":
    main()
