from time import perf_counter
from docplex.cp.model import CpoModel


def CP_solver(
    model: CpoModel,
    x: list[list],
    input: list[list[int]]
) -> dict:
    n = len(input)

    start_solve = perf_counter()
    solution = model.solve()
    solve_time = perf_counter() - start_solve

    result = None

    if solution:
        result = [
            [solution[x[r][c]] for c in range(n)]
            for r in range(n)
        ]


    return {
        "status": "FEASIBLE" if solution else "NO_SOLUTION",
        "solve_time": solve_time
    }