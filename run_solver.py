"""!@file run_solver.py
@brief A script for solving a sudoku board.

@details A script for solving a sudoku board. Currently accepts only
input in the form of a 9x9 or 11x11 board.

@author Created by I. Petrov on 26/11/2023
"""
import sys

from src.solver.solver import SudokuSolver
from src.logic.backtracking import NaiveBacktracker
from src.logic.singles_logic import ObviousSingles

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("No configuration passed - terminating.")
        exit()

    path = sys.argv[1]

    step_list = [ObviousSingles]
    backtracker = NaiveBacktracker

    if "." not in path:
        print("Cannot infer file extension - assuming text input.")
        board_path = path
    elif path.split(".")[-1] == "txt":
        board_path = path
    else:
        print("Did not detect configuration extension, assuming text input.")
        board_path = path

    solver = SudokuSolver(board_path, logic_rules=step_list, backtracker=backtracker)
    solver.run()
