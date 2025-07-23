from typing import Optional, Tuple
import numpy as np
from src.algorithms.strategy.mazeGenerationStrategy import MazeGenerationStrategy

class Maze:
    """
    A class representing a maze.
    The maze is represented as a 2D numpy array.
    - WALL: '0' represents a wall (blocked path)
    - PATH: '1' represents a walkable path
    - START: 'S' represents the starting point
    - END: 'E' represents the end point
    """

    WALL = '0'
    PATH = '1'
    START = 'S'
    END = 'E'

    # Constants defining the border size for the maze
    bordersHorizontal = 2
    bordersVertical = 2

    def __init__(self, width: int, height: int, generation_strategy: 'MazeGenerationStrategy',
                 isAnimation: bool = False, start: Optional[Tuple[int, int]] = None, end: Optional[Tuple[int, int]] = None):

        if width <= 0 or height <= 0:
            raise ValueError("Maze dimensions must be positive integers")

        self.width = width + self.bordersHorizontal
        self.height = height + self.bordersVertical
        self.generation_strategy = generation_strategy
        self.maze_matrix = np.zeros((self.height, self.width), dtype='U1')
        self.maze_matrix[:] = self.WALL

        self.start = start if start else (self.bordersHorizontal//2, self.bordersVertical//2)
        self.end = end if end else (self.width - self.bordersHorizontal, self.height - self.bordersVertical)

        self.isAnimation = isAnimation
        self.on_step = None

    def display_maze(self) -> None:
        """
        Prints the current maze state into console.
        """
        print(self.maze_matrix)

    def generate_maze(self) -> None:
        """
        Generates the maze using the specific generation strategy (algorithm)
        """
        if not hasattr(self.generation_strategy, 'generate_maze'):
            raise TypeError("Generation strategy must implement 'generate_maze'")
        self.generation_strategy.generate_maze(self, self.on_step if self.isAnimation else None)


    def modify_maze(self, position: Tuple[int, int], value: str) -> None:
        """
        Modifies a specific cell in the maze.
        """
        x, y = position
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"Position ({x}, {y}) is out of bounds")
        if value not in {self.WALL, self.PATH, self.START, self.END}:
            raise ValueError(f"Invalid cell value: {value}")
        self.maze_matrix[y][x] = value

    def set_callback(self, callback) -> None:
        self.on_step = callback
