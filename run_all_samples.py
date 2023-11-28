"""!@file run_all_samples.py

@brief Runs the solver on all available samples.

@details Runs the solver on all available samples. Used for determining success
in different situations, as well as for profiling.

@author Created by I. Petrov on 26/11/2023
"""
import glob
import io
import sys

from src.solver.solver import SudokuSolver

from src.logic.backtracking import SelectiveBacktracker
from src.logic.singles_logic import ObviousSingles, HiddenSingles
from src.logic.complex_logic import HiddenPointers, ObviousPairs

if __name__ == "__main__":
    step_list = [ObviousSingles, HiddenSingles, HiddenPointers, ObviousPairs]
    backtracker = SelectiveBacktracker
    visualization = "none"
    bad = []
    for directory in ["easy", "medium", "hard", "impossible", "many_solutions"]:
        total = 0
        success = 0
        text_trap = io.StringIO()
        sys.stdout = text_trap

        # Get all sample files.
        for path in glob.glob(f"./test/samples/{directory}/*.txt"):
            solver = SudokuSolver(path, step_list, backtracker, visualization)
            result = solver.run()
            if result:
                success += 1
            else:
                bad.append(path)
            total += 1
        sys.stdout = sys.__stdout__
        print(
            f"Solved {success} / {total} ({100*success/total:.2f}%) {directory} puzzles."
        )
