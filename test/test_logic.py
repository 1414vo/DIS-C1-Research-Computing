"""!@file test_parsing.py
@brief Unit tests for validating logic modules.

@details Unit tests for validating logic modules. Checks whether each logic module
correctly finds the signal it was designed for.

@author Created by I. Petrov on 26/11/2023
"""
import numpy as np
from src.solver.board import Board
from src.logic.singles_logic import ObviousSingles, HiddenSingles
from src.logic.complex_logic import HiddenPointers, ObviousPairs


def test_obvious_singles_block():
    """! Tests the Obvious singles rule implementation for a block. Given the board below,
    the module should find the first number in the second row to be a '4', as it is
    the only possibility for the cell.
    Board:
    [1, 2, 3, 0, 0, 0, 0, 0, 0],
    [0, 4, 5, 0, 0, 0, 0, 0, 0],
    [6, 7, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]"""
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
    """! Tests the Obvious singles rule implementation for a row and a column. Given the board below,
    the module should find the last number in the first row to be a '9', as it is
    the only possibility for the cell. Similarly, it should find the last number in the
    first column to be a '4' for the same reason.
    Board:
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [9, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]"""
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


def test_hidden_singles_block():
    """! Tests the Hidden singles rule implementation for a block. Checks whether
    given the board below, the first cell of the second row is set to be a '1', as it
    is the only place in the first block where a '1' can be found.
    Board:
    [0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 4, 5, 0, 0, 0, 0, 0, 0],
    [6, 7, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]"""
    board_nums = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
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
    logic = HiddenSingles()

    logic.step(board)

    # Check if the logic has found the number
    assert board.board[1, 0] == 1


def test_hidden_singles_row():
    """! Tests the Hidden singles rule implementation for a row. Checks whether
    given the board below, the third cell of the first row is set to be a '1', as it
    is the only place in the first row where a '1' can be found.
    Board:
    [7, 0, 0, 0, 0, 0, 2, 3, 4],
    [0, 5, 6, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]"""
    board_nums = np.array(
        [
            [7, 0, 0, 0, 0, 0, 2, 3, 4],
            [0, 5, 6, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    board = Board(board_nums)
    logic = HiddenSingles()

    logic.step(board)

    # Check if the logic has found the number
    assert board.board[0, 2] == 1


def test_hidden_singles_col():
    """! Tests the Hidden singles rule implementation for a column. Checks whether
    given the board below, the second cell of the first column is set to be a '1', as it
    is the only place in the first column where a '1' can be found.
    Board:
    [7, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 6, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 0]"""
    board_nums = np.array(
        [
            [7, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 6, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 0, 0, 0, 0, 0],
            [4, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    board = Board(board_nums)
    logic = HiddenSingles()

    logic.step(board)

    # Check if the logic has found the number
    assert board.board[1, 0] == 1


def test_hidden_pointers():
    """! Tests the Hidden pointers rule implementation for 3-cell pointers. Checks that
    the numbers 7,8,9 are removed as possibilities for all cells in the third row and seventh
    column which are not in the 1st or 9th block.
    Board:
    [1, 2, 3, 0, 0, 0, 0, 0, 0],
    [4, 5, 6, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 1],
    [0, 0, 0, 0, 0, 0, 0, 5, 2],
    [0, 0, 0, 0, 0, 0, 0, 6, 3]"""
    board_nums = np.array(
        [
            [1, 2, 3, 0, 0, 0, 0, 0, 0],
            [4, 5, 6, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 1],
            [0, 0, 0, 0, 0, 0, 0, 5, 2],
            [0, 0, 0, 0, 0, 0, 0, 6, 3],
        ]
    )
    board = Board(board_nums)
    logic = HiddenPointers()

    for _ in range(6):
        logic.step(board)

    for num in [7, 8, 9]:
        for i in range(6):
            assert num not in board.cell_possibilities[2, i + 3]
            assert num not in board.cell_possibilities[i, 6]


def test_hidden_pointers2():
    """! Tests the Hidden pointers rule implementation for 2-cell pointers. Checks that
    the numbers 8,9 are removed as possibilities for all cells in the third row and seventh
    column which are not in the 1st or 9th block.
    Board:
    [1, 2, 3, 0, 0, 0, 0, 0, 0],
    [4, 5, 6, 0, 0, 0, 0, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 1],
    [0, 0, 0, 0, 0, 0, 0, 5, 2],
    [0, 0, 0, 0, 0, 0, 7, 6, 3]"""
    board_nums = np.array(
        [
            [1, 2, 3, 0, 0, 0, 0, 0, 0],
            [4, 5, 6, 0, 0, 0, 0, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 1],
            [0, 0, 0, 0, 0, 0, 0, 5, 2],
            [0, 0, 0, 0, 0, 0, 7, 6, 3],
        ]
    )
    board = Board(board_nums)
    logic = HiddenPointers()

    for _ in range(4):
        logic.step(board)

    for num in [8, 9]:
        for i in range(6):
            assert num not in board.cell_possibilities[2, i + 3]
            assert num not in board.cell_possibilities[i, 6]


def test_obvious_pairs():
    """! Tests the Obvious pairs rule implementation. Because the numbers 7,9 have
    to be shared between the cells in (2nd row, 4th column) and (3rd row, 6th column),
    the possibilities for all other cells in the same block have to be discounted.
    Board:
    [0, 0, 2, 0, 8, 5, 0, 0, 4],
    [0, 0, 0, 0, 3, 0, 0, 6, 0],
    [0, 0, 4, 2, 1, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 5, 2],
    [0, 0, 0, 0, 0, 0, 3, 1, 0],
    [9, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 6, 0, 0, 0],
    [2, 5, 0, 4, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 1, 6, 0, 0]"""
    board_nums = np.array(
        [
            [0, 0, 2, 0, 8, 5, 0, 0, 4],
            [0, 0, 0, 0, 3, 0, 0, 6, 0],
            [0, 0, 4, 2, 1, 0, 0, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 5, 2],
            [0, 0, 0, 0, 0, 0, 3, 1, 0],
            [9, 0, 0, 0, 0, 0, 0, 0, 0],
            [8, 0, 0, 0, 0, 6, 0, 0, 0],
            [2, 5, 0, 4, 0, 0, 0, 0, 8],
            [0, 0, 0, 0, 0, 1, 6, 0, 0],
        ]
    )
    board = Board(board_nums)
    assert board.cell_possibilities[1, 3] == set([7, 9])
    assert board.cell_possibilities[2, 5] == set([7, 9])
    assert board.cell_possibilities[0, 3] == set([6, 7, 9])

    logic = ObviousPairs()
    logic.step(board)

    assert board.cell_possibilities[0, 3] == set([6])
