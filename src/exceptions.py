"""!@file exceptions.py
@brief Different custom exceptions for the solver.

@details Different custom exceptions for the solver. Contains an exception to handle
solving issues.

@author Created by I. Petrov on 26/11/2023
"""


class InvalidBoardException(Exception):
    """! Exception to handle an error during the solving process."""

    def __init__(self, message=""):
        super(InvalidBoardException, self).__init__(message)
