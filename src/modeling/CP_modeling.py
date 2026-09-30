from docplex.cp.model import CpoModel

def CP_modeling(input: list[list[int]])->tuple[CpoModel, list[list[int]]]:
   n = len(input)
   model = CpoModel()
   #Variable 
   x = [
      [model.integer_var(1, n, name=f"x_{r}_{c}") for c in range(n)]
      for r in range(n)
   ]

   #Row constrain
   for r in range(n):
     model.add(model.all_diff(x[r]))

   #Column constrain
   for c in range(n):
     model.add(model.all_diff(x[c]))

   #Block constrain
   block_size = int(n**0.5)
   for br in range(block_size):
     for bc in range(block_size):
       block = [
           x[br*block_size+r][bc*block_size+c]
           for r in range(block_size)
           for c in range(block_size)
       ]
       model.add(model.all_diff(block))

   #Given clue
   for r in range(n):
     for c in range(n):
       value = input[r][c]
       if value!=0:
         model.add(x[r][c] == value)

   return model, x              
