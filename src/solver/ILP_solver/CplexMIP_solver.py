from time import perf_counter
from docplex.mp.model import Model


def cplexmip_solver(
    model: Model,
    var: dict,
    input: list[list[int]]
) -> dict:
    n = len(input)

    start_solve = perf_counter()
    solution = model.solve()
    solve_time = perf_counter() - start_solve

    result = None

    if solution is not None:
        result = [[0] * n for _ in range(n)]

        for r in range(n):
            for c in range(n):
                for d in range(1, n + 1):
                    if solution.get_value(var[r, c, d]) > 0.5:
                        result[r][c] = d
                        break

    return {
        "status": "FEASIBLE" if solution is not None else "NO_SOLUTION",
        "solve_time": solve_time
    }