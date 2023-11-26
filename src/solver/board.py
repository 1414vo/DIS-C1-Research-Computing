"""!@file board.py
@brief A structure representing the state of the board.

@details A structure representing the state of the board. It is responsible for keeping
consistent representations of the correct numbers, as well as all possibilites for each cell.

@author Created by I. Petrov on 26/11/2023
"""

import numpy as np


def get_block_indeces(row, col):
    block_id = (row // 3, col // 3)
    return [
        (block_id[0] * 3 + i, block_id[1] * 3 + j) for i in range(3) for j in range(3)
    ]


class Board:
    """! The class representing a board state.
    Is able to keep track of possibilities for each cell and also receive updates
    on the board state.
    """

    def __init__(self, board: np.ndarray) -> None:
        """! Creates a board state from an initial matrix.

        @param board - The initial parsed configuration. Must be a 9x9 NumPy array.
        @throws ValueError - if passed board is not of the correct shape or type.
        """

        if type(board) != np.ndarray or board.shape != (9, 9):
            raise ValueError("Invalid board type or shape passed to Board class.")

        self.board = np.zeros((9, 9), dtype=np.int8)

        for i in range(9):
            for j in range(9):
                if board[i, j] != 0:
                    self.update(i, j, board[i, j])

    def __format_row(self, row: np.ndarray) -> str:
        """! Creates a string representation of a board row for visualisation.

        @param row - a particular row of the board.
        """
        out = ""
        for i, item in enumerate(row):
            out += str(item)
            # Add a block boundary column
            if i % 3 == 2 and i != 8:
                out += "|"
        return out + "\n"

    def __str__(self) -> str:
        """! Creates a string representation of the board."""
        out = ""
        for i, row in enumerate(self.board):
            out += self.__format_row(row)
            # Add a block boundary row.
            if i % 3 == 2 and i != 8:
                out += "---+---+---\n"

        return out

    def get_possibilities(self) -> np.ndarray:
        """! Computes the possibilities for the value in each cell."""
        cell_possibilities = np.array(
            [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]
        )
        for i in range(9):
            for j in range(9):
                if self.board[i, j] != 0:
                    cell_possibilities[i, j] = set([self.board[i, j]])
                for num in range(1, 10):
                    if num in self.board[i, :]:
                        cell_possibilities[i, j].discard(num)
                        continue
                    if num in self.board[:, j]:
                        cell_possibilities[i, j].discard(num)
                        continue
                    block_x, block_y = i // 3, j // 3
                    if (
                        num
                        in self.board[
                            block_x * 3 : block_x * 3 + 3, block_y * 3 : block_y * 3 + 3
                        ]
                    ):
                        cell_possibilities[i, j].discard(num)
        return cell_possibilities

    def update(self, row: int, col: int, value: int) -> None:
        """! Enters a value for a particular cell if possible.

        @ param row - The row of the cell.
        @ param col - The column of the cell.
        @ param value - The value to be inserted.

        @throws ValueError - If one tries to update a cell for which the value is impossible.
        """
        if value not in self.get_possibilities()[row, col]:
            raise ValueError(
                "Attempting to set a value that has been removed as an option."
            )
        self.board[row, col] = value

    def is_solved(self) -> bool:
        """! Checks if the state is solved. Assumes that consistent checks have been performed."""
        return np.all(self.board != 0)
