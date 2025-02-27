"""!@file test_parsing.py
@brief Unit tests for validating the parsing procedure.

@details Unit tests for validating the parsing procedure. Contains at least 1 test
for each of the core steps - reading, cleaning, preprocessing and validation. Also validates
that the process fails correctly, so that mis-inputs are caught and addressed correctly.

@author Created by I. Petrov on 25/11/2023
"""
from src.exceptions import InvalidBoardException, InvalidStepException
import src.parsing.validation as validation
import src.parsing.sudoku_parser as sudparser
import src.parsing.config_parsing as cfg_parser
import numpy as np
import os

from src.logic.singles_logic import ObviousSingles
from src.logic.backtracking import SelectiveBacktracker


def test_failures() -> None:
    """! Tests whether validation can detect different error types. Checks
    that the implementation correctly requires that a consistently square board is
    provided, and that the board is of size 9x9/11x11(with symbols for boundaries)."""
    caught_all_failures = True

    one_row_board = [["0", "1", "2"]]
    try:
        validation.check_input_validity(one_row_board)

        # If there is no error detected, the program will
        # continue to the next line and fail the test
        caught_all_failures = False
    except InvalidBoardException:
        pass

    diff_line_length_board = [["0", "1"], ["0", "1", "2"]]
    try:
        validation.check_input_validity(diff_line_length_board)

        # If there is no error detected, the program will
        # continue to the next line and fail the test
        caught_all_failures = False
    except InvalidBoardException:
        pass

    three_by_three_board = [["0", "1", "2"], ["0", "1", "2"], ["0", "1", "2"]]
    try:
        validation.check_input_validity(three_by_three_board)

        # If there is no error detected, the program will
        # continue to the next line and fail the test
        caught_all_failures = False
    except InvalidBoardException:
        pass

    assert caught_all_failures


def test_read() -> None:
    """! Tests whether the read_board function has been correctly implemented. Loads from the sample sudoku
    from the sample sudoku file and separates the characters in an array."""
    dir = os.path.dirname(os.path.realpath(__file__))
    board = sudparser.read_board(f"{dir}/samples/sample_sudoku.txt")
    assert board == [
        ["0", "0", "0", "|", "0", "0", "7", "|", "0", "0", "0"],
        ["0", "0", "0", "|", "0", "0", "9", "|", "5", "0", "4"],
        ["0", "0", "0", "|", "0", "5", "0", "|", "1", "6", "9"],
        ["-", "-", "-", "+", "-", "-", "-", "+", "-", "-", "-"],
        ["0", "8", "0", "|", "0", "0", "0", "|", "3", "0", "5"],
        ["0", "7", "5", "|", "0", "0", "0", "|", "2", "9", "0"],
        ["4", "0", "6", "|", "0", "0", "0", "|", "0", "8", "0"],
        ["-", "-", "-", "+", "-", "-", "-", "+", "-", "-", "-"],
        ["7", "6", "2", "|", "0", "8", "0", "|", "0", "0", "0"],
        ["1", "0", "3", "|", "9", "0", "0", "|", "0", "0", "0"],
        ["0", "0", "0", "|", "6", "0", "0", "|", "0", "0", "0"],
    ]


def test_9_x_9() -> None:
    """! Tests whether the pipeline can parse a clean 9x9 input. Determines that the
    pipeline correctly handles the 9x9 case."""
    dir = os.path.dirname(os.path.realpath(__file__))
    board = sudparser.parse(f"{dir}/samples/sample_9x9.txt")
    assert np.all(
        board
        == np.array(
            [
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                [2, 3, 4, 5, 6, 7, 8, 9, 1],
                [3, 4, 5, 6, 7, 8, 9, 1, 2],
                [4, 5, 6, 7, 8, 9, 1, 2, 3],
                [5, 6, 7, 8, 9, 1, 2, 3, 4],
                [6, 7, 8, 9, 1, 2, 3, 4, 5],
                [7, 8, 9, 1, 2, 3, 4, 5, 6],
                [8, 9, 1, 2, 3, 4, 5, 6, 7],
                [9, 1, 2, 3, 4, 5, 6, 7, 0],
            ]
        )
    )


def test_11_x_11() -> None:
    """! Tests whether the pipeline can parse a clean 11x11 input.Determines that the
    pipeline correctly handles the 11x11 case."""
    dir = os.path.dirname(os.path.realpath(__file__))
    board = sudparser.parse(f"{dir}/samples/sample_11x11.txt")
    assert np.all(
        board
        == np.array(
            [
                [1, 2, 0, 4, 5, 6, 7, 8, 9],
                [2, 3, 4, 5, 6, 7, 8, 9, 1],
                [3, 4, 5, 6, 7, 8, 9, 1, 2],
                [4, 5, 6, 7, 0, 9, 1, 2, 3],
                [5, 6, 7, 8, 9, 1, 2, 3, 4],
                [6, 7, 8, 9, 1, 2, 3, 4, 5],
                [7, 0, 9, 1, 2, 3, 4, 5, 6],
                [8, 9, 1, 2, 3, 4, 5, 6, 7],
                [9, 1, 2, 3, 4, 5, 6, 7, 0],
            ]
        )
    )


def test_cleaning() -> None:
    """! Tests whether the pipeline can clean up a board with different artifacts. Determines that
    different line lengths are handled correctly, alongside leading/preceding spaces."""
    dir = os.path.dirname(os.path.realpath(__file__))
    board = sudparser.parse(f"{dir}/samples/noisy_11x11.txt")
    assert np.all(
        board
        == np.array(
            [
                [1, 2, 0, 4, 5, 6, 7, 8, 9],
                [2, 3, 4, 5, 6, 7, 8, 9, 1],
                [3, 4, 5, 6, 7, 8, 9, 1, 2],
                [4, 5, 6, 7, 0, 9, 1, 2, 3],
                [5, 6, 7, 8, 9, 1, 2, 3, 4],
                [6, 7, 8, 9, 1, 2, 3, 4, 5],
                [7, 0, 9, 1, 2, 3, 4, 5, 6],
                [8, 9, 1, 2, 3, 4, 5, 6, 7],
                [9, 1, 2, 3, 4, 5, 6, 7, 0],
            ]
        )
    )


def test_config_parsing():
    """! Tests whether the configuration parser behaves
    correctly on valid input. The assertions must match the provided sample configuration.
    """

    cfg_info = cfg_parser.parse_config("test/configs/sample_config.ini")
    board_path, output_path, step_list, backtracker, visualization = cfg_info

    assert board_path == "./test/samples/sample_sudoku.txt"
    assert len(step_list) == 4
    assert step_list[0] == ObviousSingles
    assert backtracker == SelectiveBacktracker
    assert visualization == "animate"
    assert output_path == "./output/sample_test.sol"


def test_config_inference():
    """! Tests whether the configuration parser behaves
    correctly on valid input with missing categories. If said categories are missing,
    the defaults must be used."""

    cfg_info = cfg_parser.parse_config("test/configs/sample_config_2.ini")
    board_path, output_path, step_list, backtracker, visualization = cfg_info

    assert board_path == "test/sample_sudoku.txt"
    assert len(step_list) == 4
    assert step_list[0] == ObviousSingles
    assert backtracker == SelectiveBacktracker
    assert visualization == "none"
    assert output_path[:8] == "./output"


def test_config_errors():
    """! Tests whether the configuration parser correctly
    detects invalid configurations."""
    try:
        _ = cfg_parser.parse_config("test/configs/sample_config_3.ini")
        assert False
    except InvalidStepException:
        assert True
