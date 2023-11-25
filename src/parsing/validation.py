"""!@file validation.py
@brief Contains a method to validate the raw input.

@details Contains a method to validate the raw input. In particular, it determines whether
the board is 'mostly' square - i.e. a square shape can be inferred., and if it is
the correct shape for a sudoku board.
@author Created by I. Petrov on 25/11/2023
"""
import numpy as np


def check_input_validity(board: np.ndarray) -> None:
    """! Determines whether the raw input is valid enough to be inferred to be a sudoku board.
    The following steps are performed:
    1. Determine whether the shape is rectangular.
    2. Determine whether the shape is square.
    3. The board is of shape resembling a sudoku board(9x9 or 11x11).

    @param board - A NumPy array containing the cleaned board.

    @throws ValueError if one of the checks is not passed. A message descr
    """
    line_length = len(board[0])

    # Check if shape is rectangular.
    for i in range(1, len(board)):
        if len(board[i]) != line_length:
            raise ValueError(
                "Input rows contain a different number of elements - cannot infer board structure. Exiting."
            )

    # Check if shape is square.
    if len(board) != len(board[0]):
        raise ValueError(
            f"Provided board should be square, received ({len(board)}, {len(board[0])}) "
            + "- true shape could not be inferred. Exiting"
        )

    # Check if board is of shape 9x9(only numbers) or 11x11(with block boundaries)
    if not len(board) in [9, 11]:
        msg = (
            "Input should be a 9x9 sudoku board(containing only the numbers)"
            + " or 11x11 (containing the block boundaries). "
            + f"Instead received a block of shape ({len(board)}, {len(board[0])})"
        )

        raise ValueError(msg)
