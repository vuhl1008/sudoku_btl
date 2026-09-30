from pysat.card import CardEnc, EncType

def var(r:int, c:int, d:int, n:int)-> int:
    return n**2*r + n*c + d

def add_sequential_amo(literals: list[int], clauses: list[list[int]], next_var:int) -> int:
     cnf = CardEnc.atmost(
         lits = literals,
         bound = 1,
         encoding=EncType.seqcounter,
         top_id = next_var-1
     )
     clauses.extend(cnf.clauses)

     return cnf.nv + 1

def sequential_encode(input:list[list[int]])-> list[list[int]]:
    clauses = []
    n = len(input)
    #ALO
    for r in range(n):
        for c in range(n):
            literals = [
                var(r, c, d, n)
                for d in range(1, n+1)
            ]

            clauses.append(literals)

    next_var = n**3 + 1

    #AMO for each cell
    for r in range(n):
        for c in range(n):
            literals = [
                var(r, c, d, n)
                for d in range(1, n+1)
            ]
            next_var = add_sequential_amo(
                literals,
                clauses,
                next_var
            )


    #AMO for each row
    for r in range(n):
        for d in range(1, n+1):
            literals = [
                var(r, c, d, n)
                for c in range(n)
            ]                
            next_var = add_sequential_amo(
                literals,
                clauses,
                next_var
            )


    #AMO for each column
    for c in range(n):
        for d in range(1, n+1):
            literals = [
                var(r, c, d, n)
                for r in range(n)
            ]
            next_var = add_sequential_amo(
                literals,
                clauses,
                next_var
            )


    #AMO for each block
    block_size = int(n**0.5)
    for br in range(block_size):
        for bc in range(block_size):
            for d in range(1, n+1):
                literals = [
                    var(
                        br*block_size + r,
                        bc*block_size + c,
                        d,
                        n
                    )
                    for r in range(block_size)
                    for c in range(block_size)
                ]

                next_var = add_sequential_amo(
                    literals,
                    clauses,
                    next_var
                )
                

    #Add clues from the input board 
    for r in range(n):
        for c in range(n):
            val = input[r][c]
            if val != 0:
                literals = [
                    var(r, c, val, n)
                ]
                clauses.append(literals)

    return clauses                