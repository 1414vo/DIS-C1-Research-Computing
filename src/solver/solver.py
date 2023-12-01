"""!@file solver.py
@brief Contains the core class for executing a Sudoku solver.

@details Contains the core class for executing a Sudoku solver.
It is configurable by a set of rules and a backtracking algorithm.
The rules are executed sequentially and if there is no result, the backtracker is called to make a guess.

@author Created by I. Petrov on 26/11/2023
"""
import copy
from typing import List
import src.parsing.sudoku_parser as sudparser
from src.solver.board import Board
from src.exceptions import InvalidBoardException

from src.logic.base_logic import BaseLogic, BaseBacktracker
from src.logic.backtracking import NaiveBacktracker
from src.logic.singles_logic import ObviousSingles

from src.animation import animate


class SudokuSolver:
    """! The core class for executing a solution for a board."""

    def __init__(
        self,
        file_path: str,
        logic_rules: List[BaseLogic] = None,
        backtracker: BaseBacktracker = NaiveBacktracker,
        visualization: str = "none",
    ):
        """! Creates a solver wrapper for solving a board and displaying the sudoku logic.

        @param file_path - The path to the file containing the board.
        @param logic_rules - A list of logic rules.
        @param backtracker - The backtracking algorithm to apply when a deadlock is reached.
        @param visualization - What type of visualization to use."""

        self.is_solvable = None

        self.print_results = visualization == "text"
        self.store_states = visualization == "animate"

        # Read from given file
        try:
            board_value = sudparser.parse(file_path)
        except InvalidBoardException:
            print("Invalid input setup - sudoku has no solution")
            self.is_solvable = False
            return
        except FileNotFoundError:
            print(f"Could not find file {file_path}.")
            self.is_solvable = False
            return

        # Attempt board setup
        try:
            self.board = Board(board_value)
            print("Final preprocessed board:")
            print(self.__str__())
        except InvalidBoardException:
            print("Invalid board setup - sudoku has no solution")
            self.is_solvable = False
            return

        # Store states for animation
        if self.store_states:
            self.board_states = [self.board.board.copy()]
            self.possibility_states = [copy.deepcopy(self.board.cell_possibilities)]

        # Register logic rules - if not specified, use inferred most optimal set.
        if logic_rules is None:
            self.logic_rules = [ObviousSingles]
        else:
            self.logic_rules = logic_rules

        self.backtracker = backtracker

    def attempt_backtrack(self, backtracker: BaseBacktracker) -> bool:
        """! Attempts to backtrack a single step.

        @param backtracker - The instance of a backtracking algorithm.

        @return Whether the backtracking succeeded.
        """
        try:
            backtracker.backtrack(self.board)
            return True
        except InvalidBoardException:
            print("Backtracking failed: the board has no solution.")
            return False

    def execute_step(
        self, rules: List[BaseLogic], backtracker: BaseBacktracker
    ) -> bool:
        """! Tries to execute a single solution step. All logic rules are attempted initially
        before passing the board to the backtracker. If one of the rules fails, we attempt backtracking
        to the previous valid state.

        @param rules - A list of logic rule instances.
        @param backtracker - The instance of a backtracking algorithm.

        @return Whether the sudoku was solved after the step.
        """
        backtrack_result = True
        rule_result = False

        # Execute rules sequentially
        for rule in rules:
            try:
                rule_result = rule.step(self.board)
            except InvalidBoardException:
                if self.print_results:
                    print("Board failed - backtracking to previous state.")
                # If there was an issue with executing a rule - attempt backtracking or fail otherwise.
                backtrack_result = self.attempt_backtrack(backtracker)
            # End step if board is not solved and rule has succeeded
            if rule_result and not self.board.is_solved():
                break
            elif rule_result:
                print("Solution found:")
                print(self.board)
                return True

        # If last rule failed (meaning all failed), backtracker makes a guess.

        if not rule_result:
            try:
                backtracker.step(self.board)
            except InvalidBoardException:
                backtrack_result = self.attempt_backtrack(backtracker)

        if not backtrack_result:
            return False

        return None

    def run(self, max_steps: int = 300000) -> bool:
        """! Executes steps sequentially until either a solution is reached or a lot of time has passed.

        @param max_steps - The maximum amount of steps the
        @return Whether the solver succeeded.
        """
        if not self.is_solvable and self.is_solvable is not None:
            print("The board has no solution")
            return False
        # Instantiate rules and backtracker

        rules = []
        for rule in self.logic_rules:
            rules.append(rule(print_results=self.print_results))

        backtracker = self.backtracker(print_results=self.print_results)

        n_steps = 0

        while self.is_solvable is None and n_steps < max_steps:
            step_result = self.execute_step(rules, backtracker)

            if self.store_states:
                self.board_states.append(self.board.board.copy())
                self.possibility_states.append(
                    copy.deepcopy(self.board.cell_possibilities)
                )

            n_steps += 1

            if step_result is not None:
                if self.store_states:
                    animate(self.board_states, self.possibility_states)
                return step_result
            
        print(f"Could not find solution within {max_steps}.")
        return False
    
    def get_solution(self):
        if not self.board.is_solved():
            return None
        
        return self.board

    def __str__(self):
        """! Creates a string representation of the current state."""
        return self.board.__str__()
