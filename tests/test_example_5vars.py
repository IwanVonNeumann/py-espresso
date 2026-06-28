from py_espresso.minimize import minimize_greedy
from py_espresso.problem import BooleanProblem


def test_minimize_greedy_5vars_example():
    problem = BooleanProblem(
        n=5,
        on={1, 3, 5, 7, 9, 13, 17, 21, 25, 29},
        dc={0, 4, 12, 16, 20, 24, 28},
    )

    solution = minimize_greedy(problem)

    assert solution.is_valid(problem)
    assert solution.is_complete(problem)
    assert solution.is_solution(problem)

    assert solution.patterns() == [
        "---01",
        "00--1",
    ]

    assert solution.cube_count() == 2
    assert solution.literal_count() == 5
    assert solution.cost() == (2, 5)
