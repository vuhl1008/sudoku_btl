import time
from src.processing.parse_input import read_file, parse
from src.processing.validator import validate_board
from src.modeling.SAT_encoding.sequential_encoding import sequential_encode
from src.modeling.SAT_encoding.pairwise_encoding import pairwise_encode
from src.modeling.CP_modeling import CP_modeling
from src.modeling.ILP_modeling.Gurobi_modeling import gurobi_modeling
from src.modeling.ILP_modeling.CplexMIP_modeling import cplexmip_modeling
from src.solver.SAT_solver import sat_solver
from src.solver.CP_solver import CP_solver
from src.solver.ILP_solver.gurobi_solver import gurobi_solver
from src.solver.ILP_solver.CplexMIP_solver import cplexmip_solver


def validate_input(file_path):
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
def SAT_solving_with_pairwise(board: list[list[int]]) -> dict:
    start_encoding = time.perf_counter()
    clauses = pairwise_encode(board)
    encoding_time = time.perf_counter() - start_encoding

    res_sat = sat_solver(board, clauses)

    res_sat["construction_time"] = (
        encoding_time + res_sat["loading_time"]
    )

    res_sat["total_time"] = res_sat['total_time'] + encoding_time

    return res_sat

def SAT_solving_with_sequential(board:list[list[int]])-> list[list[int]]:
       
       start_encoding = time.perf_counter()
       clauses = sequential_encode(board)
       encoding_time = time.perf_counter() - start_encoding
   
       res_sat = sat_solver(board, clauses)
   
       res_sat["construction_time"] = (
           encoding_time + res_sat["loading_time"]
       )
   
       res_sat["total_time"] = res_sat['total_time'] + encoding_time
   
       return res_sat


#CP_solving
def CP_solving(board:list[list[int]]) -> list[list[int]]:
   start_time = time.perf_counter()
   model, x = CP_modeling(board)
   construction_time = time.perf_counter() - start_time
   res_cp = CP_solver(model, x, board)
   res_cp['construction_time'] = construction_time
   res_cp['total_time'] = res_cp['solve_time'] + construction_time

   return res_cp

#ILP_solving with gurobi
def gurobi_solving(board:list[list[int]]) -> list[list[int]]:
   start_time = time.perf_counter()
   model, var = gurobi_modeling(board)
   construction_time = time.perf_counter() - start_time
   res_gurobi = gurobi_solver(model, var, board)
   res_gurobi['construction_time'] = construction_time
   res_gurobi['total_time'] = res_gurobi['solve_time'] + construction_time

   return res_gurobi

#ILP_solving with CPLEX MIP
def cplexmip_solving(board:list[list[int]]) -> list[list[int]]:
   start_time = time.perf_counter()
   model, var = cplexmip_modeling(board)
   construction_time = time.perf_counter() - start_time
   res_cplexmip = cplexmip_solver(model, var, board)
   res_cplexmip['construction_time'] = construction_time
   res_cplexmip['total_time'] = res_cplexmip['solve_time'] + construction_time

   return res_cplexmip


