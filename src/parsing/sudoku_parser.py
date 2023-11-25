"""!@file sudoku_parser.py
@brief Contains the core methods for parsing a sudoku board input.

@details Contains the core methods for parsing a sudoku board input. It combines
the separate parsing modules, including opening the file, pre-processing and validation of the input.
@author Created by I. Petrov on 25/11/2023
"""

from typing import List


def read_board(file_path: str) -> List[List[chr]]:
    """! Reads the raw data into a 2D grid. Ignores the new line character if it exists

    @param file_path: The path to where the text file, containing the board is located.

    @return A parsed 2D grid, with each line being stored as a list of characters.
    @throws FileNotFoundException if the file has not been found.
    """
    print(f"Reading {file_path}")
    board = []
    with open(file_path, "r") as f:
        out = ""
        for line in f:
            out += line
            board.append([*line] if line[-1] != "\n" else [*line[:-1]])
        print(f"Raw data: \n{out}")
    return board
