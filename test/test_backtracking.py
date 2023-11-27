import numpy as np
import copy
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
    current_possibilities = copy.deepcopy(board.get_possibilities())
    logic = NaiveBacktracker()
    logic.step(board)

    assert board.board[0, 0] != 0

    logic.backtrack(board)

    current_possibilities[0, 0].discard(1)
    assert np.all(board_nums == board.board)
    assert np.all(current_possibilities == board.get_possibilities())
