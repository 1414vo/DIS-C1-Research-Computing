"""!@file test_parsing.py
@brief Unit tests for validating logic modules.

@details Unit tests for validating logic modules.

@author Created by I. Petrov on 26/11/2023
"""
import numpy as np
from src.solver.board import Board
from src.logic.singles_logic import ObviousSingles


def test_obvious_singles_block():
    """! Tests the Obvious singles rule implementation for a block"""
    board_nums = np.array(
        [
            [1, 2, 3, 0, 0, 0, 0, 0, 0],
            [0, 4, 5, 0, 0, 0, 0, 0, 0],
            [6, 7, 8, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    board = Board(board_nums)
    logic = ObviousSingles()

    logic.step(board)

    assert board.board[1, 0] == 9


def test_obvious_singles_row_col():
    """! Tests the Obvious singles rule implementation for a row and a column"""
    board_nums = np.array(
        [
            [1, 2, 3, 4, 5, 6, 7, 8, 0],
            [5, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 0],
            [8, 0, 0, 0, 0, 0, 0, 0, 0],
            [9, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    board = Board(board_nums)
    logic = ObviousSingles()

    logic.step(board)
    logic.step(board)

    assert board.board[0, 8] == 9
    assert board.board[8, 0] == 4
