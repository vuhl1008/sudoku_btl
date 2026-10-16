from pysat.card import CardEnc, EncType

def add_pairwise_encoding(literals:list[int], clauses: list[list[int]])-> None:

    cnf = CardEnc.atmost(
        lits=literals,
        bound=1,
        encoding=EncType.pairwise
    )

    clauses.extend(cnf.clauses)

    return 
def pairwise_encode(input:list[list[int]]) -> list[list[int]]:

    n = len(input)
    clauses = []

    #AMO+ALO for each cell
    for r in range(n):
        for c in range(n):
            literals = [
               r*n*n + c*n + d
               for d in range(1, n+1) 
            ]
            clauses.append(literals)
            add_pairwise_encoding(
                literals,
                clauses
            )

    #AMO+ALO for each row
    for r in range(n):
        for d in range(1, n+1):
            literals = [
                r*n*n + c*n + d
                for c in range(n)
            ]
            clauses.append(literals)
            add_pairwise_encoding(
                literals,
                clauses
            )    

    #AMO+ALO for each col
    for c in range(n):
        for d in range(1, n+1):
            literals = [
                r*n*n + c*n + d
                for r in range(n)
            ]
            clauses.append(literals)
            add_pairwise_encoding(
                literals,
                clauses
            )

    #AMO+ALO for each block
    block_size = int(n**0.5)
    for br in range(block_size):
        for bc in range(block_size):
            for d in range(1, n+1):
                literals = [
                   (block_size*br + r)*n*n + 
                   (block_size*bc + c)*n +
                   d
                   for r in range(block_size)
                   for c in range(block_size) 
                ]
                clauses.append(literals)
                add_pairwise_encoding(
                    literals,
                    clauses
                )

    #Given clues
    for r in range(n):
        for c in range(n):
            val = input[r][c]
            if val!=0:
                literals = [
                    r*n*n + c*n + val
                ]
            clauses.append(literals)    

    return clauses        