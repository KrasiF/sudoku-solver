from sudoku_solver import SudokuSolver

sudoku1 = [["",8,"",2,"",4,"","",5],
          ["","","",7,"","","","",""],
          ["",4,6,"","","",1,"",""],
          ["","",5,"",8,"","","",6],
          [8,2,"","","","","",7,""],
          [1,"",3,"","","","",8,9],
          ["",9,4,"","","","","",""],
          [5,"",8,"","","","",3,""],
          ["","","",8,"","",2,"",""]]

sudoku2 = [["",4,"",8,"","","","",6],
          ["","",1,"","",6,"","",3],
          ["","",6,3,"",9,8,"",""],
          [2,5,"",6,"",3,"","",""],
          ["","","","","","","","",""],
          ["",8,7,"","","","",4,""],
          ["","","","",9,"",7,"",""],
          ["","","","","",4,"",1,""],
          ["","","","","",2,"","",5]]

sudoku3 = [["","","","","","","",8,""],
          [9,4,"","","",7,"","",""],
          ["","",5,"","","","",1,""],
          ["",1,"",2,"",8,"",4,""],
          ["","","",6,"","",7,"",""],
          [7,"","","","","","","",9],
          [1,2,"",9,"","","","",""],
          ["","","","","",5,"","",""],
          ["",7,4,1,"","","","",6]]

def run():
    welcome()
    get_sudoku_input_loop()
    try_another_dialogue()

def welcome():
    print("Welcome to the showcase of my Sudoku Solver! This is the version without an ASCII grid*")
    print("Choose a number from 1 to 3 to display and then solve one of three example sudokus.")

def get_sudoku_input_loop():
    sudoku_to_solve = None
    inp = input()
    while sudoku_to_solve is None:
        if inp == "1":
            sudoku_to_solve = sudoku1
        elif inp == "2":
            sudoku_to_solve = sudoku2
        elif inp == "3":
            sudoku_to_solve = sudoku3
        else:
            print("Please enter a valid number.")
            inp = input()
    get_sudoku_results(sudoku_to_solve)
    
def get_sudoku_results(sudoku_to_solve):
    solver = SudokuSolver(sudoku_to_solve)
    print("Originally:")
    print(sudoku_to_solve)
    print("Solved:")
    print(solver.solve_sudoku())

def try_another_dialogue():
    print("Want to have another go? Type \"y\" for yes.")
    inp = input()
    if inp == "y":
        run()

run()