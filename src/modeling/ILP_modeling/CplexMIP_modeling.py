from docplex.mp.model import Model

def cplexmip_modeling(input:list[list[int]])->tuple[Model, dict]:
    n = len(input)
    model = Model(name='Sudoku')

    #Initalize variables
    var = model.binary_var_dict(
        [(r, c, d)
        for r in range(n)
        for c in range(n)
        for d in range(1, n+1)],
        name='var'
    )

    #==========#
    #Constrains
    #==========#

    #Each cell
    for r in range(n):
        for c in range(n):
            model.add_constraint(
                model.sum(
                    var[r,c,d] for d in range(1, n+1)
                ) == 1
            )

    #Each row
    for r in range(n):
        for d in range(1, n+1):
            model.add_constraint(
                model.sum(
                    var[r,c,d] for c in range(n)
                ) == 1
            )

    #Each col
    for c in range(n):
        for d in range(1, n+1):
            model.add_constraint(
                model.sum(
                    var[r,c,d] for r in range(n)
                ) == 1
            )

    #Each block
    block_size = int(n**0.5)
    for br in range(block_size):
        for bc in range(block_size):
            for d in range(1, n+1):
                model.add_constraint(
                    model.sum(
                        var[br*block_size+r, bc*block_size+c, d]
                        for r in range(block_size)
                        for c in range(block_size)
                    ) == 1
                )  

    #Given clues
    for r in range(n):
        for c in range(n):
            val = input[r][c]
            if val!=0:
                model.add_constraint(
                    var[r,c,val] == 1
                )

    return model, var                                              