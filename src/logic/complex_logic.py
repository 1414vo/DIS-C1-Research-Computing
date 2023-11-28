"""!@file complex_logic.py
@brief Logic components that operate on multiple cells.

@details Logic components that operate on multiple cells. Currently includes the Hidden pointers rule.

@author Created by I. Petrov on 28/11/2023
"""
from src.sudoku_utils.steps.BaseLogic import BaseLogic
from src.sudoku_utils.Board import Board
import numpy as np
from typing import Tuple


class HiddenPointers(BaseLogic):
    """! A class implementing the detction of the Hidden pointers rule."""

    def __init__(self, print_results: bool = False):
        """! Creates a logic rule to apply the Hidden pointers rule.

        @param print_results - A configuration parameter on whether to print the step results.
        """
        super(HiddenPointers, self).__init__(print_results)
        self.name = "HiddenPointers"

        # Keep memory of detected pointers, so as to not repeat actions.
        self.applied_pointers = [set() for _ in range(9)]

    def print_msg(self, find_type: str, idx: int, num: int):
        """! Prints the finding of the logic rule if text-based reporting is allowed.

        @param find_type - Whether the signal was found in a column, row or block.
        @param idx - The index of the row, column or block.
        @param num - The value of the signal found.
        """
        if self.print_results:
            print(f"Found hidden pointer of number {num} in {find_type} {idx + 1}.")

    def __check_block(self, block: int, num: int) -> Tuple[str, int]:
        """! Private method for checking a block for a given signal.

        @param block - The values of the block.
        @param num - The value of the signal to be checked.

        @return A pair of values - one for the finding type - row or column. The second is the index of the
        relevant row/column. If there is no signal, the first value of the tuple is None.
        """
        has_num = [[num in cell for cell in row] for row in block]
        in_col = np.sum(has_num, axis=0)
        if np.all(sorted(in_col) == [0, 0, 3]) or np.all(sorted(in_col) == [0, 0, 2]):
            return "column", in_col.argmax()
        in_row = np.sum(has_num, axis=1)
        if np.all(sorted(in_row) == [0, 0, 3]) or np.all(sorted(in_row) == [0, 0, 2]):
            return "row", in_row.argmax()

        return None, 0

    def __clean_row(self, board: Board, row: int, block_col: int, num: int):
        """! Removes the possibilities from the given row.

        @param board - The current board state.
        @param row - The index of the row.
        @param block_col - The column index of the block. All values within the block will be ignored.
        @param num - The value of the signal found"""
        for i in range(9):
            if i // 3 != block_col:
                board.cell_possibilities[row, i].discard(num)

    def __clean_col(self, board: Board, col: int, block_row: int, num: int):
        """! Removes the possibilities from the given column.

        @param board - The current board state.
        @param row - The index of the column.
        @param block_col - The row index of the block. All values within the block will be ignored.
        @param num - The value of the signal found"""
        for i in range(9):
            if i // 3 != block_row:
                board.cell_possibilities[i, col].discard(num)

    def step(self, board: Board) -> bool:
        """! Attempts to make progress on the board. Checks if a block contains
        values only on a given row/column and removes all possibilities from the other blocks.

        @param board - The board to attempt progress on.

        @return Whether the step succeeded.
        """
        for i in range(9):
            block_x, block_y = i // 3, i % 3
            for num in range(1, 10):
                if num in self.applied_pointers[i]:
                    continue
                action, idx = self.__check_block(
                    board.get_possibilities()[
                        3 * block_x : 3 * block_x + 3, 3 * block_y : 3 * block_y + 3
                    ],
                    num,
                )
                if action == "column":
                    self.applied_pointers[i].add(num)
                    self.__clean_col(board, block_y * 3 + idx, block_x, num)
                    self.print_msg("column", block_y * 3 + idx, num)

                    return True

                if action == "row":
                    self.applied_pointers[i].add(num)
                    self.__clean_row(board, block_x * 3 + idx, block_y, num)
                    self.print_msg("row", block_x * 3 + idx, num)

                    return True

        return False
