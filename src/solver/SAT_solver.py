from time import perf_counter
from pysat.solvers import Solver


def sat_solver(
    input: list[list[int]],
    clauses: list[list[int]],
) -> dict:
    n = len(input)

    start_total = perf_counter()

    start_loading = perf_counter()
    with Solver(name="kissat", bootstrap_with=clauses) as solver:
        loading_time = perf_counter() - start_loading

        start_solve = perf_counter()
        status = solver.solve()
        solve_time = perf_counter() - start_solve

        try:
            stats = solver.accum_stats()
        except NotImplementedError:
            stats = None

        solution = None


        if status:
            model = solver.get_model()
            solution = [[0] * n for _ in range(n)]

            for v in model:
                if 0 < v <= n**3:
                    v_idx = v - 1
                    r = v_idx // n**2
                    c = (v_idx % n**2) // n
                    d = (v_idx % n) + 1
                    solution[r][c] = d

            final_status = "SAT"
        else:
            final_status = "UNSAT"

    return {
        "status": final_status,
        "loading_time": loading_time,
        "solve_time": solve_time,
        "total_time": perf_counter() - start_total,
        "stats": stats,
    }