"""!@file animation.py
@brief Helper functions for animating a sudoku solution.

@details Helper functions for animating a sudoku solution. They are able to display
the initial board, the found numbers, as well as the remaining possibilities in a cell.

@author Created by I. Petrov on 27/11/2023
"""
import numpy as np
from typing import List
from matplotlib import axes
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt


def draw_state(
    board: np.ndarray,
    possibilities: np.ndarray,
    initial_setup: np.ndarray,
    ax: axes.Axes,
):
    """! Creates a snapshot plot of a given state. Initial numbers are
    displayed in black, found ones in blue and possibile cell options are
    displayed in a 3x3 grid.

    @param board - A grid of solved numbers. If a cell is still unsolved, a 0 is expected.
    @param possibilities - A grid of sets containing the remaining possibilities for each cell
    @param initial_setup - A mask showing whether each cell has been initially set to some number.
    @param ax - The axes the image should be plotted on.
    """
    ax.clear()
    ax.set(xlim=(0, 1), ylim=(0, 1))
    for i in range(1, 9):
        # Draws the cell boundaries (wider if on the block boundary)
        ax.axhline(i / 9, linewidth=2 if i % 3 != 0 else 3.5, color="black")
        ax.axvline(i / 9, linewidth=2 if i % 3 != 0 else 3.5, color="black")

    for i in range(9):
        for j in range(9):
            if board[i, j] != 0:
                # Draws a solved cell
                ax.text(
                    1 / 18 + j * 1 / 9,
                    17 / 18 - i * 1 / 9,
                    str(board[i, j]),
                    fontsize=18,
                    horizontalalignment="center",
                    verticalalignment="center",
                    color="black" if initial_setup[i, j] else "tab:blue",
                )
            else:
                # Draws an unsolved cell
                for num in range(9):
                    num_x, num_y = num % 3, num // 3
                    if num + 1 in possibilities[i, j]:
                        ax.text(
                            1 / 54 + num_x * 1 / 27 + j * 1 / 9,
                            1 - (1 / 54 + num_y * 1 / 27 + i * 1 / 9),
                            str(num + 1),
                            fontsize=6,
                            horizontalalignment="center",
                            verticalalignment="center",
                            color="gray",
                        )
    ax.grid(False)
    ax.axis("off")


def animate(state_seq: List[np.ndarray], possibility_seq: List[np.ndarray]):
    """! Animates a sequence of board states.

    @param state_seq - A sequence of board states.
    @param possibility_seq - A sequence of cell possibilities.
    """
    fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
    plt.axis("off")
    # Obtain the mask for whether a value was initially set for each cell.
    initial_setup = np.where(state_seq[0] != 0, True, False)

    def animate_frame(i=0):
        """! Helper function for generating a FuncAnimation animation.
        Draws a single state from the sequence."""
        draw_state(state_seq[i], possibility_seq[i], initial_setup, ax=ax)

    ani = FuncAnimation(
        fig,
        animate_frame,
        frames=len(state_seq),
        init_func=animate_frame,
        interval=1500,
        repeat=False,
    )

    plt.show()
    return ani
