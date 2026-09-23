def validate_structure(board: list[list[int]]) -> None:
    if not isinstance(board, list):
        raise TypeError("Board must be a list.")

    n = len(board)

    if n == 0:
        raise ValueError("Board must not be empty.")

    root = int(n ** 0.5)
    if root * root != n:
        raise ValueError("Board size must be a perfect square.")

    for row in board:
        if not isinstance(row, list):
            raise TypeError("Each row must be a list.")

        if len(row) != n:
            raise ValueError(f"Board must have size {n}x{n}.")

        for value in row:
            if type(value) is not int:
                raise TypeError(f"Cell value {value!r} must be an int.")

            if not 0 <= value <= n:
                raise ValueError(
                    f"Cell value {value} must be between 0 and {n}."
                )


def validate_rows(board)->None:
    n = len(board)
    for r in range(n):
        values = [
            board[r][c]
            for c in range(n)
            if board[r][c] != 0
        ]
        if len(values) != len(set(values)):
            raise ValueError('Duplicate value in a row')

def validate_columns(board)->None:
    n = len(board)
    for c in range(n):
        values = [
            board[r][c] 
            for r in range(n) 
            if board[r][c]!=0
        ]
        if len(values)!=len(set(values)):
            raise ValueError('Duplicate value in a column')

def validate_blocks(board)->None:
    n=len(board)
    block_size = int(n**0.5)
    for row in range(0, n, block_size):
        for col in range(0, n, block_size):
            values=[]
            for i in range(row, row+block_size):
                for j in range(col, col+block_size):
                    if board[i][j]!=0:
                        values.append(board[i][j])

            if len(values) != len(set(values)):
                raise ValueError(f"Duplicate value in a {block_size}x{block_size} block")

def validate_board(board)->None:
    validate_structure(board)
    validate_rows(board)
    validate_columns(board)
    validate_blocks(board)