# Sudoku Solver - ivp24

This repository contains a solver for a $9\times 9$ Sudoku board.

## Table of contents
1. [Requirements](#requirements)
2. [Setup](#setup)
3. [Running the solver](#running-the-solver)
4. [Features](#features)
5. [Frameworks](#frameworks)
6. [Build status](#build-status)
7. [Credits](#credits)

## Requirements

The user should have a version of Docker installed in order to ensure correct setup of environments. If that is not possible, please ensure you have all the specified packages in the `environment.yml` file correct.

## Setup

To correctly set up the environment, we utilise a Docker image. To build the image before creating the container, you can run.

`docker build -t ivp24_sudoku .`

The setup image will also add the necessary pre-commit checks to your git repository, ensuring the commits work correctly.

Afterwards, any time you want to use the code, you can launch a Docker container using:

`docker run --rm -ti ivp24_sudoku`

If you want to make changes to the repository, you would likely need to use your Git credentials. A safe way to load your SSH keys was to use the following command:

`docker run --rm -v <ssh folder on local machine>:/root/.ssh -ti ivp24_sudoku`

This copies your keys to the created container and you should be able to run all required git commands.

## Running the solver

There are 2 different ways to run the solver. If you want to run a single sudoku puzzle, you can either:
- Provide only a text file containing the board. The solver will not display any steps made during the solution, and will use the optimal setup.
This includes all logic rules, alongside the `Selective backtracker`. An example board can be seen in `test\samples\sample_sudoku.txt`.
- Provide a full configuration, as seen in `test/configs/sample_config.ini`. You can specify both the solver configuration, as well as the visualization method. Accepted visualization methods include a text-based representation and a matplotlib animation.

## Features

The solver supports different methods of solving, all specified by a set and order of logic rules and backtracking.
A solver must always contain a set of logic rules, (perhaps empty - but this might take too long to run), and a single backtracking algorithm.
The logic rules must be chosen among `Obvious Singles`, `Hidden Singles`, `Hidden Pointers`, `Obvious Pairs`. More details on them can be found on [the Sudoku.com website]("https://sudoku.com/sudoku-rules").
The backtracking algorithms available are a simple **Naive backtracker**, as well as a "smarter" **Selective backtracker**. The latter is
recommended as it can save a substantial amount of backtracking steps, and is not significantly more computationally expensive.

## Frameworks

The entire project was built on **Python** and uses the following packages:
- For computation and parsing:
    - NumPy
    - configparser
- For plotting:
    - matplotlib
- For maintainability/documentation:
    - doxygen
    - pytest
    - pre-commit

## Build status
Currently, the build is in an experimentation phase and may not be stable.

## Credits

The `.pre-commit-config.yaml` configuration file content has been adapted from the Research Computing lecture notes.
Ideas for the logic rules were taken from [the Sudoku.com website]("https://sudoku.com/sudoku-rules").
The example sudoku boards were found from [Dimitri Fontaine's Git repository]("https://github.com/dimitri/sudoku/tree/master") and
[Sudopedia]("http://sudopedia.enjoysudoku.com/Invalid_Test_Cases.html").
