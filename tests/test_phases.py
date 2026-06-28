from py_espresso.cover import Cover
from py_espresso.cube import Cube
from py_espresso.expand import expand_cover_greedy
from py_espresso.irredundant import make_irredundant_greedy
from py_espresso.minimize import minimize_espresso_greedy, minimize_greedy
from py_espresso.problem import BooleanProblem
from py_espresso.reduce import reduce_cover_greedy


def example_problem() -> BooleanProblem:
    return BooleanProblem(
        n=5,
        on={1, 3, 5, 7, 9, 13, 17, 21, 25, 29},
        dc={0, 4, 12, 16, 20, 24, 28},
    )


def test_reduce_preserves_solution():
    problem = example_problem()
    solution = minimize_greedy(problem)

    reduced = reduce_cover_greedy(solution, problem)

    assert reduced.is_valid(problem)
    assert reduced.is_complete(problem)
    assert reduced.is_solution(problem)


def test_expand_preserves_validity():
    problem = example_problem()
    reduced = reduce_cover_greedy(minimize_greedy(problem), problem)

    expanded = expand_cover_greedy(reduced, problem)

    assert expanded.is_valid(problem)
    assert not expanded.covered_off(problem)


def test_irredundant_preserves_solution_and_removes_redundant_cube():
    problem = example_problem()
    redundant_cover = Cover(
        [
            Cube.from_pattern("---01"),
            Cube.from_pattern("00--1"),
            Cube.from_pattern("00101"),
        ]
    )

    irredundant = make_irredundant_greedy(redundant_cover, problem)

    assert redundant_cover.is_solution(problem)
    assert irredundant.is_solution(problem)
    assert irredundant.cube_count() < redundant_cover.cube_count()


def test_espresso_greedy_zero_iterations_matches_greedy_baseline():
    problem = example_problem()

    greedy = minimize_greedy(problem)
    espresso_zero_iter = minimize_espresso_greedy(problem, max_iter=0)

    assert espresso_zero_iter.patterns() == greedy.patterns()
    assert espresso_zero_iter.cost() == greedy.cost()
