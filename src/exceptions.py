"""!@file exceptions.py
@brief Different custom exceptions for the solver.

@details Different custom exceptions for the solver. Contains exceptions to handle
issues during the solving process and during the configuration parsing.

@author Created by I. Petrov on 26/11/2023
"""


class InvalidBoardException(Exception):
    """! Exception to handle an error during the solving process. Can be used during any point
    of the solving process."""

    def __init__(self, message=""):
        super(InvalidBoardException, self).__init__(message)


class InvalidStepException(Exception):
    """! Exception to handle an error in specifying the logic/backtracking
    steps in the configuration. Should be returned if the defined step does not exist.
    """

    def __init__(self, message=""):
        super(InvalidStepException, self).__init__(message)
