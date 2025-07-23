import random
from typing import Literal
from src.maze.maze import Maze
from src.algorithms.strategy.mazeGenerationStrategy import MazeGenerationStrategy

class RecursiveDivisionAlgorithm(MazeGenerationStrategy):
    """
    A class implementing the Recursive Division algorithm for maze generation.
    This algorithm starts with empty grid (full of paths - chamber). Divides the chamber with randomly
    position wall where each wall contains randomly positioned passage opening within it. Then recursively
    repeats the process on the subchambers until all chambers are minimum sized.
    This method results in maze with long straight walls crossing their space.
    """
    def __init__(self):
        pass

    def generate_maze(self, maze: Maze, on_step=None) -> None:
        self.on_step = on_step
        self.maze = maze
        self.width = self.maze.width
        self.height = self.maze.height

        # Fill the maze with open paths (excluding border walls)
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                self.maze.maze_matrix[y][x] = '1'

        # Begin recursive division
        self.divide(1, 1, self.width - 2, self.height - 2, self.chooseOrientation(self.width - 2, self.height - 2))

    def divide(self, x: int, y: int, width: int, height: int, orientation: Literal["Horizontal", "Vertical"]) -> None:
        """
        Recursively divides a rectangular region with a wall and a passage.
        """
        # Base case
        if width < 3 or height < 3:
            return

        horizontal = orientation == "Horizontal"

        if horizontal:
            # Choose a horizontal wall position (odd row index)
            wall_y = y + (random.randrange(0, height // 2)) * 2 + 1
            # Choose a passage (even column index)
            passage_x = x + (random.randrange(0, width // 2 + 1)) * 2

            # Build horizontal wall with one passage
            for wx in range(x, x + width):
                if wx == passage_x:
                    self.maze.maze_matrix[wall_y][wx] = '1'
                else:
                    self.maze.maze_matrix[wall_y][wx] = '0'
                self.animation()

            # Recursively divide above and below
            self.divide(x, y, width, wall_y - y, self.chooseOrientation(width, wall_y - y))
            self.divide(x, wall_y + 1, width, y + height - wall_y - 1, self.chooseOrientation(width, y + height - wall_y - 1))

        else:  # vertical
            # Choose a vertical wall position (odd column index)
            wall_x = x + (random.randrange(0, width // 2)) * 2 + 1
            # Choose a passage (even row index)
            passage_y = y + (random.randrange(0, height // 2 + 1)) * 2

            # Build vertical wall with one passage
            for wy in range(y, y + height):
                if wy == passage_y:
                    self.maze.maze_matrix[wy][wall_x] = '1'
                else:
                    self.maze.maze_matrix[wy][wall_x] = '0'
                self.animation()

            # Recursively divide left and right
            self.divide(x, y, wall_x - x, height, self.chooseOrientation(wall_x - x, height))
            self.divide(wall_x + 1, y, x + width - wall_x - 1, height, self.chooseOrientation(x + width - wall_x - 1, height))

    def chooseOrientation(self, width: int, height: int) -> Literal["Horizontal", "Vertical"]:
        """
        Choose orientation based on region dimensions
        """
        if width < height:
            return "Horizontal"
        elif height < width:
            return "Vertical"
        else:
            return random.choice(["Horizontal", "Vertical"])

    def animation(self) -> None:
        """
        Triggers animation callback if provided.
        """
        if self.on_step:
            self.on_step(self.maze.maze_matrix)
