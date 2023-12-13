"""!@file test_board.py
@brief Unit tests for validating the board generation and possibility computation.

@details Unit tests for validating the board generation and possibility computation.
Verifies whether the board is correctly initialized and whether updating causes correct
possibility recomputation.

@author Created by I. Petrov on 26/11/2023
"""

import numpy as np
from src.solver.board import Board


def test_board_initialization() -> None:
    """! Tests whether correctly after initialization, the board correctly has
    the correct number values and cell possibilities. Given the board below,
    determines whether the bottom right corner has only the possibility of an '8' left.
    Board:
    [0, 0, 0, 0, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 5],
    [0, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 9],
    [9, 1, 2, 3, 4, 5, 6, 7, 0]"""
    board_nums = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 7],
            [0, 0, 0, 0, 0, 0, 0, 0, 6],
            [0, 0, 0, 0, 0, 0, 0, 0, 5],
            [0, 0, 0, 0, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 3],
            [0, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 9],
            [9, 1, 2, 3, 4, 5, 6, 7, 0],
        ]
    )
    board = Board(board_nums)
    # Check if first 8 lines are properly initialized
    assert np.all(board.board[:-1] == board_nums[:-1])

    cell_possibilities = board.get_possibilities()
    # Check if all possibilities for lower right corner have been eliminated
    assert len(cell_possibilities[8, 8]) == 1
    # Check if the remaining possibility is 8
    assert 8 in cell_possibilities[8, 8]


def test_board_update():
    """! Tests whether the board implementation correctly handles updating an empty
    board's top left cell. The board should then have the cell possibilities in the
    given row, column and block updated.
    """
    board_nums = np.zeros((9, 9))
    board = Board(board_nums)
    board.update(0, 0, 7)

    assert board.board[0, 0] == 7
    cell_possibilities = board.get_possibilities()
    for i in range(1, 9):
        # Check column updates
        assert 7 not in cell_possibilities[i, 0]
        # Check row updates
        assert 7 not in cell_possibilities[0, i]
        # Check block updates
        assert 7 not in cell_possibilities[i % 3, i // 3]
