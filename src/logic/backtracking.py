"""!@file backtracking.py
@brief Logic components that utilise a backtracking algorithm.

@details Logic components that utilise a backtracking algorithm. Currently contains
a naive backtracking algorithm, which guesses arbitrarily.

@author Created by I. Petrov on 26/11/2023
"""
from src.logic.base_logic import BaseBacktracker
from src.exceptions import InvalidBoardException
from src.solver.board import Board
import copy
import numpy as np


class NaiveBacktracker(BaseBacktracker):
    """! A class for simple backtracking."""

    def __init__(self, print_results=False):
        """! Creates a simple backtracker.

        @param print_results - A configuration parameter on whether to print the step results.
        """
        super(NaiveBacktracker, self).__init__(print_results)
        self.name = "NaiveBacktracker"

    def step(self, board: Board) -> bool:
        """! Attempts to make progress on the board. Attempts to guess a possibility on the first
        possible unsolved sell.

        @param board - The board to attempt progress on.
        @throws - InvalidBoardException if the backtracker finds a cell with no possibilities.

        @return Whether the step succeeded.
        """
        for i in range(9):
            for j in range(9):
                if board.board[i, j] == 0:
                    cell_possibilities = board.get_possibilities()
                    if len(cell_possibilities[i, j]) == 0:
                        raise InvalidBoardException("No option for number selection")
                    num = next(iter(cell_possibilities[i, j]))

                    # Store the previous board state
                    self.board_memory.append(board.board.copy())
                    self.cell_pos_memory.append(
                        copy.deepcopy(board.get_possibilities())
                    )
                    self.guess_memory.append((i, j, num))
                    
                    # Update the board based on the guess
                    board.update(i, j, num)
                    self.print_msg(i + 1, j + 1, num, board)
                    return True

        return False


class SelectiveBacktracker(BaseBacktracker):
    """! A class for improved selection backtracking."""

    def __init__(self, print_results: bool = False):
        """! Creates a selective backtracker.

        @param print_results - A configuration parameter on whether to print the step results.
        """
        super(SelectiveBacktracker, self).__init__(print_results)
        self.name = "SelectiveBacktracker"

    def step(self, board):
        """! Attempts to make progress on the board. Attempts to guess a possibility on the most
        defined cell, i.e. the cell with the least number of options

        @param board - The board to attempt progress on.
        @throws - InvalidBoardException if the backtracker finds a cell with no possibilities.

        @return Whether the step succeeded.
        """
        # Obtain the number of possibilities per cell
        n_possibilities = np.vectorize(len)(board.cell_possibilities)
        n_possibilities = np.where(
            (n_possibilities == 1) & (board.board != 0), 10, n_possibilities
        )

        # Get the indeces of the best cell.
        i, j = np.unravel_index(n_possibilities.argmin(), (9, 9))

        # If there is a cell with no possibilities, report the error.
        if len(board.cell_possibilities[i, j]) == 0:
            raise InvalidBoardException("No option for number selection")

        
        num = next(iter(board.cell_possibilities[i, j]))
        
        # Store previous state in memory
        self.board_memory.append(board.board.copy())
        self.cell_pos_memory.append(copy.deepcopy(board.cell_possibilities))
        self.guess_memory.append((i, j, num))
        
        # Update the board with the new guess.
        board.update(i, j, num)
        self.print_msg(i + 1, j + 1, num, board)
