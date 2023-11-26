"""!@file singles_logic.py
@brief Logic components that operate on single cells.

@details Logic components that operate on single cells. Currently includes the Obvious singles rule.

@author Created by I. Petrov on 26/11/2023
"""
from src.logic.base_logic import BaseLogic
from src.solver.board import Board


class ObviousSingles(BaseLogic):
    """! A class implementing the detction of the Obvious singles rule."""

    def __init__(self, print_results: bool = False):
        """! Creates a logic rule to apply the Obvious singles rule.

        @param print_results - A configuration parameter on whether to print the step results.
        """
        super(ObviousSingles, self).__init__(print_results)
        self.name = "ObviousSingles"

    def step(self, board: Board) -> bool:
        """! Attempts to make progress on the board. Checks if some cell
        conatins only a single possibility and updates it if so.

        @param board - The board to attempt progress on.

        @return Whether the step succeeded.
        """
        cell_possibilities = board.get_possibilities()
        for i in range(9):
            for j in range(9):
                if board.board[i, j] == 0 and len(cell_possibilities[i, j]) == 1:
                    cell_value = next(iter(cell_possibilities[i, j]))
                    board.update(i, j, cell_value)
                    self.print_msg(i + 1, j + 1, cell_value, board)
                    return True

        return False
