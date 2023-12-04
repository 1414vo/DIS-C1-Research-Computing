"""!@file run_solver.py
@brief A script for solving a sudoku board.

@details A script for solving a sudoku board. Currently accepts only
input in the form of a 9x9 or 11x11 board.

@author Created by I. Petrov on 26/11/2023
"""
import sys
import src.parsing.config_parsing as cfg_parse
from src.solver.solver import SudokuSolver
from src.logic.backtracking import SelectiveBacktracker
from src.logic.singles_logic import ObviousSingles, HiddenSingles
from src.logic.complex_logic import HiddenPointers, ObviousPairs
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("No configuration passed - terminating.")
        exit()

    path = sys.argv[1]

    step_list = [ObviousSingles, HiddenSingles, HiddenPointers, ObviousPairs]
    backtracker = SelectiveBacktracker
    visualization = "none"
    output_path = None
    
    if "." not in path:
        print("Cannot infer file extension - assuming text input.")
        print("Cannot specify output folder using text input. Will not store output.")
        board_path = path
    elif path.split(".")[-1] == "ini":
        board_path, output_path, step_list, backtracker, visualization = cfg_parse.parse_config(path)
    elif path.split(".")[-1] == "txt":
        print("Cannot specify output folder using text input. Will not store output.")
        board_path = path
    else:
        print("Did not detect configuration extension, assuming text input.")
        print("Cannot specify output folder using text input. Will not store output.")
        board_path = path

    solver = SudokuSolver(
        board_path,
        logic_rules=step_list,
        backtracker=backtracker,
        visualization=visualization,
    )
    success = solver.run()
    
    # Print solution upon reaching it.
    if success and output_path is not None:
        try:
            output_str = str(solver.get_solution())
            with open(output_path, "w") as f:
                f.write(output_str)
        except OSError:
            print(f"Could not open file {output_path}")
            exit(1)
        
