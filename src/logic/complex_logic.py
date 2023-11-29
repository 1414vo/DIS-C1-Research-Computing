"""!@file complex_logic.py
@brief Logic components that operate on multiple cells.

@details Logic components that operate on multiple cells. Currently includes the Hidden pointers rule.

@author Created by I. Petrov on 28/11/2023
"""
from src.logic.base_logic import BaseLogic
from src.solver.board import Board
import numpy as np
from typing import Tuple, Set


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
        has_num = np.array([[num in cell for cell in row] for row in block])

        in_col = np.sum(has_num, axis=0)
        # To avoid re-computation
        max_col = in_col.argmax()
        if np.count_nonzero(in_col) == 1 and in_col[max_col] != 1:
            return "column", max_col

        in_row = np.sum(has_num, axis=1)
        # To avoid re-computation
        max_row = in_row.argmax()
        if np.count_nonzero(in_row) == 1 and in_row[max_row] != 1:
            return "row", max_row

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


class ObviousPairs(BaseLogic):
    """! A class implementing the detction of the Obvious pairs rule."""

    def __init__(self, print_results: bool = False):
        """! Creates a logic rule to apply the Obvious pairs rule.

        @param print_results - A configuration parameter on whether to print the step results.
        """
        super(ObviousPairs, self).__init__(print_results)
        self.name = "ObviousPairs"

        # Keeps track of which numbers have succeeded with checks, so we do not
        # redo the computation.
        self.pair_memory = {
            "row": {i: set() for i in range(9)},
            "col": {i: set() for i in range(9)},
            "block": {i: set() for i in range(9)},
        }

    def print_msg(self, find_type: str, idx: int, nums: int):
        """! Prints the finding of the logic rule if text-based reporting is allowed.

        @param find_type - Whether the signal was found in a column, row or block.
        @param idx - The index of the row, column or block.
        @param num - The value of the signal found.
        """
        if self.print_results:
            print(
                f"Found Obvious Pair {tuple(nums)} in {find_type} {idx + 1}.\
                   Removing all instances from {find_type}."
            )

    def __clean_row(
        self, board: Board, row: int, idxs: Tuple[int, int], nums: Set[int]
    ):
        """! Clean the row for the found pair.

        @param board - The current board state.
        @param row - The index of the row containing the pair.
        @param idxs - The column indeces of the relevant row.
        @param nums - The 2 values in the pair.
        """
        self.pair_memory["row"][row].add(tuple(sorted(nums)))
        for i in range(9):
            # Ignore the relevant pair
            if i in idxs:
                continue
            board.cell_possibilities[row, i] = board.cell_possibilities[row, i] - nums

    def __check_row(self, board: Board, row: int) -> bool:
        """! Checks a row for a hidden pair

        @param board - The current board state.
        @param row - The index of the row containing the pair.

        @return Whether the check succeeded.
        """
        for i in range(9):
            # If the cell contains only 2 values,...
            if len(board.cell_possibilities[row, i]) != 2:
                continue
            # Or if it has already been checked - skip
            elif (
                tuple(sorted(board.cell_possibilities[row, i]))
                in self.pair_memory["row"][row]
            ):
                continue
            for j in range(i + 1, 9):
                if board.cell_possibilities[row, i] == board.cell_possibilities[row, j]:
                    self.__clean_row(
                        board, row, [i, j], board.cell_possibilities[row, i]
                    )
                    self.print_msg("row", row, board.cell_possibilities[row, i])
                    return True

        return False

    def __clean_col(
        self, board: Board, col: int, idxs: Tuple[int, int], nums: Set[int]
    ):
        """! Clean the column for the found pair.

        @param board - The current board state.
        @param row - The index of the column containing the pair.
        @param idxs - The row indeces of the relevant row.
        @param nums - The 2 values in the pair.
        """
        self.pair_memory["col"][col].add(tuple(sorted(nums)))
        for i in range(9):
            if i in idxs:
                continue
            board.cell_possibilities[i, col] = board.cell_possibilities[i, col] - nums

    def __check_col(self, board: Board, col: int) -> bool:
        """! Checks a column for a hidden pair.

        @param board - The current board state.
        @param col - The index of the column containing the pair.

        @return Whether the check succeeded.
        """
        for i in range(9):
            # If the cell contains only 2 values,...
            if len(board.cell_possibilities[i, col]) != 2:
                continue
            # Or if it has already been checked - skip
            elif (
                tuple(sorted(board.cell_possibilities[i, col]))
                in self.pair_memory["col"][col]
            ):
                continue
            for j in range(i + 1, 9):
                if board.cell_possibilities[i, col] == board.cell_possibilities[j, col]:
                    self.__clean_col(
                        board, col, [i, j], board.cell_possibilities[i, col]
                    )
                    self.print_msg("column", col, board.cell_possibilities[i, col])
                    return True

        return False

    def __clean_block(
        self, board: Board, block: int, idxs: Tuple[int, int], nums: Set[int]
    ):
        """! Clean the block for the found pair.

        @param board - The current board state.
        @param block - The index of the block containing the pair.
        @param idxs - The cell indeces of the relevant (flattened) block.
        @param nums - The 2 values in the pair.
        """
        self.pair_memory["block"][block].add(tuple(sorted(nums)))
        block_x, block_y = (block // 3) * 3, (block % 3) * 3
        for i in range(9):
            if i in idxs:
                continue
            board.cell_possibilities[block_x + i // 3, block_y + i % 3] = (
                board.cell_possibilities[block_x + i // 3, block_y + i % 3] - nums
            )

    def __check_block(self, board: Board, block: int) -> bool:
        """! Checks a column for a hidden pair.

        @param board - The current board state.
        @param col - The index of the column containing the pair.

        @return Whether the check succeeded.
        """
        block_x, block_y = (block // 3) * 3, (block % 3) * 3

        for i in range(9):
            i_coords = block_x + i // 3, block_y + i % 3

            # If the cell contains only 2 values,...
            if len(board.cell_possibilities[i_coords]) != 2:
                continue
            # Or if it has already been checked - skip
            elif (
                tuple(sorted(board.cell_possibilities[i_coords]))
                in self.pair_memory["block"][block]
            ):
                continue
            for j in range(i + 1, 9):
                if (
                    board.cell_possibilities[i_coords]
                    == board.cell_possibilities[block_x + j // 3, block_y + j % 3]
                ):
                    self.__clean_block(
                        board, block, [i, j], board.cell_possibilities[i_coords]
                    )
                    self.print_msg("block", block, board.cell_possibilities[i_coords])
                    return True

        return False

    def step(self, board: Board):
        """! Attempts to make progress on the board. Checks if a block contains
        values only on a given row/column and removes all possibilities from the other blocks.

        @param board - The board to attempt progress on.

        @return Whether the step succeeded.
        """
        success = False

        for i in range(9):
            row_result = self.__check_row(board, i)
            col_result = self.__check_col(board, i)
            block_result = self.__check_block(board, i)

            if not success:
                success = row_result or col_result or block_result

        return success
