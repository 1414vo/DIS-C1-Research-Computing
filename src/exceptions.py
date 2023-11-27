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


class InvalidStepException(Exception):
    """! Exception to handle an error in specifying the logic
    steps in the configuration."""

    def __init__(self, message=""):
        super(InvalidStepException, self).__init__(message)
