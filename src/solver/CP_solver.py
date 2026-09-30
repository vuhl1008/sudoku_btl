from docplex.cp.model import CpoModel

def CP_solver(model:CpoModel, x:list[list[int]], input:list[list[int]])->list[list[int]]:
    solution = model.solve()
    n = len(input)
    if not solution:
        return 'No solution'

    result = [
        [solution[x[r][c]] for r in range(n)]
        for c in range(n)
    ]

    return result