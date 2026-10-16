import gurobipy as gp
from gurobipy import Model, tupledict
from time import perf_counter


from gurobipy import GRB

def get_gurobi_status(model):
    status_names = {
        GRB.OPTIMAL: "OPTIMAL",
        GRB.INFEASIBLE: "INFEASIBLE",
        GRB.UNBOUNDED: "UNBOUNDED",
        GRB.INF_OR_UNBD: "INF_OR_UNBD",
        GRB.TIME_LIMIT: "TIME_LIMIT",
        GRB.INTERRUPTED: "INTERRUPTED",
        GRB.SUBOPTIMAL: "SUBOPTIMAL",
    }
    return status_names.get(model.Status, f"STATUS_{model.Status}")

def gurobi_solver(
    model: Model,
    var: tupledict,
    input: list[list[int]]
) -> dict:
    n = len(input)

    start_solve = perf_counter()
    model.optimize()
    solve_time = perf_counter() - start_solve

    result = None

    if model.SolCount > 0:
        result = [[0] * n for _ in range(n)]

        for r in range(n):
            for c in range(n):
                for d in range(1, n + 1):
                    if var[r, c, d].X > 0.5:
                        result[r][c] = d
                        break

    return {
        "status": get_gurobi_status(model),
        "solve_time": solve_time,
    }