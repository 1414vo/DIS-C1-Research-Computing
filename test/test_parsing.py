"""!@file test_parsing.py
@brief Unit tests for validating the parsing procedure.

@details Unit tests for validating the parsing procedure. Contains at least 1 test
for each of the core steps - reading, cleaning, preprocessing and validation.

@author Created by I. Petrov on 25/11/2023
"""

import src.parsing.validation as validation
import src.parsing.sudoku_parser as sudparser
import os


def test_failures() -> None:
    """! Tests whether validation can detect different error types."""
    caught_all_failures = True

    one_row_board = [["0", "1", "2"]]
    try:
        validation.check_input_validity(one_row_board)

        # If there is no error detected, the program will
        # continue to the next line and fail the test
        caught_all_failures = False
    except ValueError:
        pass

    diff_line_length_board = [["0", "1"], ["0", "1", "2"]]
    try:
        validation.check_input_validity(diff_line_length_board)

        # If there is no error detected, the program will
        # continue to the next line and fail the test
        caught_all_failures = False
    except ValueError:
        pass

    three_by_three_board = [["0", "1", "2"], ["0", "1", "2"], ["0", "1", "2"]]
    try:
        validation.check_input_validity(three_by_three_board)

        # If there is no error detected, the program will
        # continue to the next line and fail the test
        caught_all_failures = False
    except ValueError:
        pass

    assert caught_all_failures


def test_read():
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
