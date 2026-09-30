from src.processing.parse_input import read_file, parse
from src.processing.validator import validate_board
from src.modeling.SAT_encoding.sequential_encoding import sequential_encode
from src.modeling.CP_modeling import CP_modeling
from src.solver.SAT_solver import sat_solver_with_sequential_encoding
from src.solver.CP_solver import CP_solver

file_path = "data/25x25_data.txt"

def validate_input():
  try:
     text = read_file(file_path)

  except FileNotFoundError as e:
     print(f"File error: {e}")
     exit()

  try:
     board = parse(text)

  except (TypeError, ValueError) as e:
     print(f"Parse error: {e}")
     exit()

  try:
     validate_board(board)

  except (TypeError, ValueError) as e:
     print(f"Validation error: {e}")
     exit()

  return board   

#SAT solving
def SAT_solving(board:list[list[int]]) -> list[list[int]]:
   clauses = sequential_encode(board)
   sat_solution = sat_solver_with_sequential_encoding(board, clauses)

   return sat_solution

def CP_solving(board:list[list[int]]) -> list[list[int]]:
   model, x = CP_modeling(board)
   CP_solution = CP_solver(model, x, board)

   return CP_solution

#CP_solving
def print_board(board):
    for row in board:
        print(" ".join(f"{x:2}" for x in row))

board = validate_input()
print('Input is valid')

solution = CP_solving(board)   

print_board(solution)