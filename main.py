from src.processing.parse_input import read_file, parse
from src.processing.validator import validate_board

file_path = "data/sudoku_data.txt"

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


def print_board(board):
    for row in board:
        print(" ".join(f"{x:2}" for x in row))

board = validate_input()
print('Input is valid')
print_board(board)