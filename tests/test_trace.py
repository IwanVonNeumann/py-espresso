from py_espresso.minimize import minimize_espresso_greedy, trace_espresso_greedy
from py_espresso.problem import BooleanProblem


def example_problem() -> BooleanProblem:
    return BooleanProblem(
        n=5,
        on={1, 3, 5, 7, 9, 13, 17, 21, 25, 29},
        dc={0, 4, 12, 16, 20, 24, 28},
    )


def test_espresso_greedy_trace_starts_with_initial_solution():
    problem = example_problem()

    trace = trace_espresso_greedy(problem)

    assert trace
    assert trace[0].iteration == 0
    assert trace[0].reason == "initial"
    assert trace[0].cover.is_solution(problem)


def test_espresso_greedy_trace_accepted_steps_improve_cost():
    problem = example_problem()
    trace = trace_espresso_greedy(problem)
    best_cost = trace[0].cover.cost()

    for step in trace[1:]:
        if step.accepted:
            assert step.candidate is not None
            assert step.candidate.cost() < best_cost
            assert step.cover.cost() == step.candidate.cost()
            best_cost = step.cover.cost()


def test_espresso_greedy_trace_final_cover_matches_minimizer():
    problem = example_problem()

    trace = trace_espresso_greedy(problem)
    solution = minimize_espresso_greedy(problem)

    assert trace[-1].cover.patterns() == solution.patterns()
    assert trace[-1].cover.cost() == solution.cost()


def test_espresso_greedy_trace_zero_iterations_has_only_initial_step():
    problem = example_problem()

    trace = trace_espresso_greedy(problem, max_iter=0)

    assert len(trace) == 1
    assert trace[0].iteration == 0
    assert trace[0].reason == "initial"
