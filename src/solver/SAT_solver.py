from src.modeling.SAT_encoding.sequential_encoding import sequential_encode
from pysat.solvers import Solver

def sat_solver_with_sequential_encoding(input:list[list[int]], clauses: list[list[int]]) -> list[list[int]]:
    with Solver(name='g3', bootstrap_with=clauses) as solver:
        n = len(input)
        if solver.solve():
            model = solver.get_model()
            solution = [[0]*n for _ in range(n)]
            for v in model:
                if 0< v <=n**3:
                    v_idx = v-1
                    r = v_idx//n**2
                    c = (v_idx%n**2) // n
                    d = (v_idx%n) + 1
                    solution[r][c] = d
            return solution
    return 'No solution'               
