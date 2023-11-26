"""!@file base_logic.py
@brief A class to be used as the basis for all logic components.

@details A class to be used as the basis for all logic components.

@author Created by I. Petrov on 26/11/2023
"""

from src.solver.board import Board


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
