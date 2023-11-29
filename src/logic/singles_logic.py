"""!@file singles_logic.py
@brief Logic components that operate on single cells.

@details Logic components that operate on single cells. Currently includes the Obvious singles
and Hidden singles rules.

@author Created by I. Petrov on 26/11/2023
"""
from src.logic.base_logic import BaseLogic
from src.solver.board import Board
import numpy as np
from typing import Tuple


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


class HiddenSingles(BaseLogic):
    """! A class implementing the detction of the Hidden singles rule."""

    def __init__(self, print_results: bool = False):
        """! Creates a logic rule to apply the Hidden singles rule.

        @param print_results - A configuration parameter on whether to print the step results.
        """
        super(HiddenSingles, self).__init__(print_results)
        self.name = "HiddenSingles"

    def __check_rows(self, board: Board) -> Tuple[int, int]:
        """! Private method for determining whether there exists a row for which
        there exists a number that can only occur in one cell.

        @param board - The current board state.
        """
        for i in range(9):
            found_nums = set(board.board[i].tolist())
            for num in range(1, 10):
                if num in found_nums:
                    continue
                num_in_cell = np.array(
                    [num in cell for cell in board.get_possibilities()[i]], dtype=bool
                )
                if np.count_nonzero(num_in_cell) == 1:
                    idx = np.argmax(num_in_cell)
                    board.update(i, idx, num)
                    return (i, idx, num)

        return None

    def __check_cols(self, board: Board) -> Tuple[int, int]:
        """! Private method for determining whether there exists a column for which
        there exists a number that can only occur in one cell.

        @param board - The current board state.
        """
        for i in range(9):
            found_nums = set(board.board[:, i].tolist())
            for num in range(1, 10):
                if num in found_nums:
                    continue
                num_in_cell = np.array(
                    [num in cell for cell in board.get_possibilities()[:, i]],
                    dtype=bool,
                )
                if np.count_nonzero(num_in_cell) == 1:
                    idx = np.argmax(num_in_cell)
                    board.update(idx, i, num)
                    return (idx, i, num)

        return None

    def __check_blocks(self, board: Board) -> Tuple[int, int]:
        """! Private method for determining whether there exists a block for which
        there exists a number that can only occur in one cell.

        @param board - The current board state.
        """
        for i in range(3):
            for j in range(3):
                found_nums = set(
                    board.board[3 * i : 3 * i + 3, 3 * j : 3 * j + 3].flatten().tolist()
                )
                for num in range(1, 10):
                    if num in found_nums:
                        continue

                    num_in_cell = np.array(
                        [
                            [num in cell for cell in row]
                            for row in board.get_possibilities()[
                                3 * i : 3 * i + 3, 3 * j : 3 * j + 3
                            ]
                        ],
                        dtype=bool,
                    )

                    if np.count_nonzero(num_in_cell) == 1:
                        idx = np.unravel_index(np.argmax(num_in_cell), (3, 3))
                        board.update(i * 3 + idx[0], j * 3 + idx[1], num)
                        return (i * 3 + idx[0], j * 3 + idx[1], num)

        return None

    def step(self, board: Board) -> bool:
        """! Attempts to make progress on the board. Checks if a row, column or block
        conatins only a single possibility for a given number and updates it if so.

        @param board - The board to attempt progress on.

        @return Whether the step succeeded.
        """
        rows_result = self.__check_rows(board)
        if rows_result:
            self.print_msg(
                rows_result[0] + 1, rows_result[1] + 1, rows_result[2], board
            )
            return True

        cols_result = self.__check_cols(board)
        if cols_result:
            self.print_msg(
                cols_result[0] + 1, cols_result[1] + 1, cols_result[2], board
            )
            return True

        block_result = self.__check_blocks(board)
        if block_result:
            self.print_msg(
                block_result[0] + 1, block_result[1] + 1, block_result[2], board
            )
            return True

        return False
