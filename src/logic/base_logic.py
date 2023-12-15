"""!@file base_logic.py
@brief Classes to be used for the basis for all logic components.

@details Classes to be used for the basis for all logic components. Includes a generic logic class, as well as
a generic backtracker class.

@author Created by I. Petrov on 26/11/2023
"""

from src.solver.board import Board
from src.exceptions import InvalidBoardException


class BaseLogic:
    """! A class to be used as the basis for all logic components."""

    def __init__(self, print_results: bool = False):
        """! Creates a base logic object - which serves a basis of other logic.
        Should not be used as a component to a solver, as it does nothing.

        @param print_results - A configuration parameter on whether to print the step results.
        """
        self.print_results = print_results
        self.name = "BaseLogic"

    def print_msg(self, row: int, col: int, num: int, board: Board) -> None:
        """! Helper function for printing an update.

        @param row - The row of the update location.
        @param col - The column of the update location.
        @param num - The number, which was put in the update.
        @param board - The relevant board data structure.
        """
        if self.print_results:
            msg = (
                f"Found Number {num} at coordinate "
                + f"{row}, {col} with method {self.name}"
            )
            print(msg)
            print(board)

    def step(self, board: Board) -> bool:
        """! Attempts to make progress on the board. For the base class, this does nothing.

        @param board - The board to attempt progress on.
        """
        pass


class BaseBacktracker(BaseLogic):
    """! A class that provides the base functionality for a backtracking algorithm."""

    def __init__(self, print_results=False):
        """! Creates a base backtracking object - which serves a basis of other backtracking algorithms.
        Should not be used as a component to a solver, as it does nothing.

        @param print_results - A configuration parameter on whether to print the step results.
        """
        super(BaseBacktracker, self).__init__(print_results)
        self.name = "BaseBacktracker"
        self.board_memory = []
        self.guess_memory = []
        self.cell_pos_memory = []

    def backtrack(self, board: Board) -> None:
        """! Restores the previous valid board state.
        @param board - The board container to modify.
        @throws InvalidBoardException - If we are at the root of the backtracking list
        - likely meaning the board has no solution.
        """
        if len(self.board_memory) == 0:
            raise InvalidBoardException("No backtracking to be undone.")
        # Recover state from memory
        board.board = self.board_memory.pop(-1)
        board.cell_possibilities = self.cell_pos_memory.pop(-1)
        last_guess = self.guess_memory.pop(-1)
        # Remove last guess from memory
        board.cell_possibilities[last_guess[0], last_guess[1]].discard(last_guess[2])
