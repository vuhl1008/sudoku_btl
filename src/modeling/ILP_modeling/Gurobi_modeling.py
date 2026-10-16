import gurobipy as gp
from gurobipy import Model, GRB

def gurobi_modeling(input:list[list[int]])-> tuple[Model, gp.tupledict]:
    n = len(input)
    #Define model
    model = gp.Model('Sudoku')

    #Initalize variables
    var = model.addVars(
        n, n, range(1, n+1),
        vtype=GRB.BINARY
    )

    #===============
    #Constrains
    #===============
    #Each cell
    for r in range(n):
        for c in range(n):
            model.addConstr(
                gp.quicksum(
                    var[r,c,d] for d in range(1, n+1)
                ) == 1
            )

    #Each row
    for r in range(n):
        for d in range(1, n+1):
            model.addConstr(
                gp.quicksum(
                    var[r,c,d] for c in range(n)
                ) == 1
            ) 

    #Each column
    for c in range(n):
        for d in range(1, n+1):
            model.addConstr(
                gp.quicksum(
                    var[r,c,d] for r in range(n)
                ) == 1
            )

    #Each block
    block_size = int(n**0.5)
    for br in range(block_size):
        for bc in range(block_size):
            for d in range(1, n+1):
                model.addConstr(
                    gp.quicksum(
                        var[br*block_size+r, bc*block_size+c, d]
                        for r in range(block_size)
                        for c in range(block_size)
                    ) == 1
                )

    #Give clues
    for r in range(n):
        for c in range(n):
            val = input[r][c]
            if val != 0:
                model.addConstr(
                    var[r,c,val] == 1
                )

    return model, var                                              

