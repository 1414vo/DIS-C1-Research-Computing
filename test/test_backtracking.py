import numpy as np
from src.solver.board import Board
from src.logic.backtracking import NaiveBacktracker


def test_naive_backtracker():
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

    logic = NaiveBacktracker()
    logic.step(board)

    assert board.board[0, 0] != 0

    logic.backtrack(board)

    assert np.all(board_nums == board.board)
