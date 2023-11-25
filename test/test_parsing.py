"""!@file test_parsing.py
@brief Unit tests for validating the parsing procedure.

@details Unit tests for validating the parsing procedure. Contains at least 1 test
for each of the core steps - reading, cleaning, preprocessing and validation.

@author Created by I. Petrov on 25/11/2023
"""

import src.parsing.validation as validation


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
