import os

def read_file(file_path:str)->str:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(file_path, 'r') as f:
        return f.read()    
    

def parse(input: str) -> List[List[int]]:
    lines = input.strip().splitlines()
    board = []
    for line in lines:
        row = [
            int(ch) if ch.isdigit() else 0
            for ch in line
        ]

        board.append(row)

    return board    
