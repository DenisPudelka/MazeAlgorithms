import random
from src.algorithms.strategy.mazeGenerationStrategy import MazeGenerationStrategy
from src.maze.maze import Maze

class WilsonAlgorithm(MazeGenerationStrategy):
    """
    Wilson's algorithm for maze generation using loop-erased random walks.
    This algorithm generates a maze with no loops and unique path between any two points by
    randomly walking from unvisited cells to the visited region and erasing loops along the way.
    We treat odd-indexed positions as valid "cells", and even-indexed positions as wall between them.
    """
    def __init__(self):
        # Wall
        self.unvisited = '0'
        # Path
        self.visited = '1'
        self.directions = [(-1,0), (1,0), (0,-1), (0,1)]


    def generate_maze(self, maze: Maze, on_step=None) -> None:
        self.on_step = on_step

        self.maze = maze
        width, height = maze.width, maze.height

        # Initialize all cells as walls
        self.maze.maze_matrix[:] = self.unvisited

        # Define which coordinates are valid "cells" (odd indices)
        def is_cell(y, x):
            return y % 2 == 1 and x % 2 == 1

        # Get all valid cell positions (odd coordinates)
        cells = [(y, x) for y in range(1, height - 1)
                 for x in range(1, width - 1)
                 if is_cell(y, x)]

        # Choose random starting cell
        start_y, start_x = random.choice(cells)
        self.maze.maze_matrix[start_y][start_x] = self.visited
        self.animation()
        self.visited_cells = {(start_y, start_x)}
        unvisited_cells = set(cells) - self.visited_cells

        while unvisited_cells:
            # Start random walk from unvisited cell
            start_walk = random.choice(list(unvisited_cells))
            path = self.walk(start_walk, self.visited_cells)

            # Carve the path
            for i in range(len(path)):
                y, x = path[i]
                self.maze.maze_matrix[y][x] = self.visited
                self.animation()
                self.visited_cells.add((y, x))
                unvisited_cells.discard((y, x))

                # Carve wall between current and previous cell
                if i > 0:
                    prev_y, prev_x = path[i - 1]
                    wall_y = (y + prev_y) // 2
                    wall_x = (x + prev_x) // 2
                    self.maze.maze_matrix[wall_y][wall_x] = self.visited
                    self.animation()


    def walk(self, start, end):
        """
        Perform a loop-erased random walk from start to the exiting visited region.
        """
        path = [start]
        current = start

        while True:
            y, x = current

            if (y, x) in self.visited_cells:
                break

            neighbors = []

            # Step size of 2 to jump to the next valid cell (skipping walls)
            for dy, dx in self.directions:
                ny, nx = y + dy * 2, x + dx * 2
                if 1 <= ny < self.maze.height - 1 and 1 <= nx < self.maze.width - 1:
                    neighbors.append((ny, nx))

            if not neighbors:
                return path

            next_cell = random.choice(neighbors)

            # If the next cell is already in our current path, erase it
            if next_cell in path:
                loop_index = path.index(next_cell)
                path = path[:loop_index + 1]
            else:
                path.append(next_cell)

            current = next_cell

        return path

    def animation(self) -> None:
        """
        Triggers animation callback.
        """
        if self.on_step:
            self.on_step(self.maze.maze_matrix)