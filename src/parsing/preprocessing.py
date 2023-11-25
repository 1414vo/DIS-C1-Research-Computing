"""!@file preprocessing.py
@brief The core methods for cleaning and re-formatting the input.

@details The core methods for cleaning and re-formatting the input. This includes
attempting to clean the lines to conform to the most likely input size, as well as
converting to a numerical format.

@author Created by I. Petrov on 25/11/2023
"""
from warnings import warn
from typing import List
import scipy.stats as stats


def clean_line(line: List[chr], length: int) -> List[chr]:
    """! Attempts to clean a line to conform to a given length.

    @param line - A list of characters, comprising a line in the raw input.
    @param length - The final line length.

    @return The best attempt of cleaning up the line.
    """
    new_line = line.copy()

    # If line is smaller than desired - pad with spaces.
    if len(new_line) < length:
        new_line += " " * (length - len(line))
        warn("Detected incomplete line - padding with empty spaces.")

    # If line is larger than desired - try to remove non-numeric entries at both ends
    elif len(new_line) > length:
        while len(new_line) != length:
            warn("Line is too long, attempting to clean trailing symbols.")
            if not new_line[-1].isnumeric():
                new_line.pop(-1)
            elif not new_line[0].isnumeric() and new_line[0] != ".":
                new_line.pop(0)
            else:
                break

    return new_line


def clean_input(board: List[List[str]]) -> List[List[str]]:
    """! Attempts to transform the input in a rectangular shape if it is not already.

    @param board - The raw input in a 2D list format.

    @return The best possible inference for a clean board. If the board is initially
    correct, it should return the same values.

    """
    line_lengths = [len(board_row) for board_row in board]

    # Assume actual width of grid is the mode.
    true_length = stats.mode(line_lengths, keepdims=False).mode

    return list(map(lambda line: clean_line(line, true_length), board))
