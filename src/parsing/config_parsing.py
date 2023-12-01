"""!@file sudoku_parser.py
@brief Contains the core methods for parsing a configuration.

@details Contains the core methods for parsing a configuration. If a certain
section is missing from the configuration, the parser will attempt to default to a
given value.

@author Created by I. Petrov on 27/11/2023
"""

import json

import configparser
from typing import List
from datetime import datetime

from src.exceptions import InvalidStepException

from src.logic.singles_logic import ObviousSingles
from src.logic.backtracking import NaiveBacktracker
from src.logic.base_logic import BaseLogic, BaseBacktracker


def string_to_step(item: str) -> BaseLogic:
    """! Transforms the name of a logic rule to the corresponding class

    @param item - The name of the rule.

    @throws InvalidStepException - if a rule with the given name does not exist.
    @return The corresponding rule class.
    """
    if item == "ObviousSingles":
        return ObviousSingles

    raise InvalidStepException(f"No step called {item} found.")


def parse_step_list(entry: List[str]) -> List[BaseLogic]:
    """! Parses a list of logic rule names.

    @param entry - A list of logic rule names.
    @return The list of logic rule classes.
    """
    entries = json.loads(entry)
    step_list = []
    for item in entries:
        step_list.append(string_to_step(item))

    return step_list


def parse_backtracker(entry: str) -> BaseBacktracker:
    """! Transforms the name of a backtracking algorithm to the corresponding class

    @param item - The name of the backtracker.
    @throws InvalidStepException - if a backtracker with the given name does not exist.
    @return The backtracking algorithm class.
    """

    if entry == "NaiveBacktracker":
        return NaiveBacktracker

    raise InvalidStepException(f"No backtracker called {entry} found.")


def parse_config(cfg_path: str):
    """! Obtains the setup for a given configuration. If possible will default
    to a set of parameters if they are not specified. The default configurations are
    to use no visualization and the best inferred rule setup.

    @param cfg_path - The location of the configuration.
    """
    cfg = configparser.ConfigParser()
    cfg.read(cfg_path)

    # Handle section existence

    if "Sudoku" not in cfg.sections():
        print(
            'No sudoku found - please specify "Sudoku" section in configuration file.'
        )
        exit()

    # Handle board path

    if "board_path" not in cfg["Sudoku"]:
        print('No board path found, field "board_path" should be non-empty.')
        exit()

    board_path = cfg["Sudoku"]["board_path"]

    # Handle visualization options

    if "visualization" not in cfg["Sudoku"]:
        print(
            "Warning: No visualization method specified - will only output final solutions."
        )
        visualization = "none"
    else:
        visualization = cfg["Sudoku"]["visualization"]

    if visualization not in ["none", "text", "animate"]:
        print(
            'Invalid visualization option - should be either "none", "text" or "animate". Defaulting to "none".'
        )
        visualization = "none"

    step_list = []

    # Handle solver configuration

    if "Solver" not in cfg:
        print(
            "Warning: No solver configuration found - defaulting to infered optimal setup"
        )
        step_list = [ObviousSingles]
        backtracker = NaiveBacktracker
    else:
        if "logic" not in cfg["Solver"]:
            print("Warning: No logic order defined - using default logic setup.")
            step_list = [ObviousSingles]
        else:
            step_list = parse_step_list(cfg["Solver"]["logic"])

        if "backtracker" not in cfg["Solver"]:
            print(
                "Warning: No backtracking algorithm specified - using NaiveBacktracker"
            )
            backtracker = NaiveBacktracker
        else:
            backtracker = parse_backtracker(cfg["Solver"]["backtracker"])
            
    if "Output" not in cfg:
        print("Warning: No output folder specified - will not save solution.")
        output_path = None
    else:
        if "output_folder" not in cfg["Output"]:
            print("Warning: No output folder specified, will store solution in \output")
            output_folder = './output'
        else:
            output_folder = cfg["Output"]["output_folder"]
            
            if output_folder[-1] in ['/', '\\']:
                print("Warning: Output folder should not end in a slash.")
                output_folder = output_folder[:-1]
        
        if "output_name" not in cfg["Output"]:
            print("Warning: No output name specified, will use current time and date.")
            now = datetime.now()
            output_name = now.strftime("%d_%m_%H_%M_%S.sol")
        else:
            output_name = cfg["Output"]["output_name"]
            
        output_path = f'{output_folder}/{output_name}'  

    return board_path, output_path, step_list, backtracker, visualization
