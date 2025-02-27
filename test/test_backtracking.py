"""!@file test_backtracking.py
@brief Unit tests for validating backtracking modules.

@details Unit tests for validating backtracking modules. Verifies that the
functionality of the backtracking algorithms is correctly implemented, i.e.
the correct cell is guessed, and the algorithm can correctly revert back to the
previous state.

@author Created by I. Petrov on 26/11/2023
"""
import numpy as np
import copy
from src.solver.board import Board
from src.logic.backtracking import NaiveBacktracker, SelectiveBacktracker


def test_naive_backtracker():
    """! Tests whether the naive backtracker makes sequential choices, and can correctly
    restore the previous state. Given the board below, we expect the top left cell to change,
    and then be reverted to the original empty state without the guessed value.
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
    current_possibilities = copy.deepcopy(board.get_possibilities())
    logic = NaiveBacktracker()
    logic.step(board)

    assert board.board[0, 0] != 0

    logic.backtrack(board)

    current_possibilities[0, 0].discard(1)
    assert np.all(board_nums == board.board)
    assert np.all(current_possibilities == board.get_possibilities())


def test_selective_backtracker():
    """! Tests whether the selective backtracker makes optimal choices, and can correctly
    restore the previous state. Given the board below, we expect any of the numbers in the last
    column or row to be selectedand then be reverted to the original empty state without the guessed value
    .
    Board:
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 5],
    [0, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 9],
    [9, 1, 2, 3, 4, 5, 6, 0, 0]"""
    board_nums = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 6],
            [0, 0, 0, 0, 0, 0, 0, 0, 5],
            [0, 0, 0, 0, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 3],
            [0, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 9],
            [9, 1, 2, 3, 4, 5, 6, 0, 0],
        ]
    )
    board = Board(board_nums)
    logic = SelectiveBacktracker()
    logic.step(board)

    print(board.board)
    cond = board.board[0, 8] != 0 or board.board[8, 8] != 0 or board.board[8, 7] != 0
    assert cond

    logic.backtrack(board)

    assert np.all(board_nums == board.board)
