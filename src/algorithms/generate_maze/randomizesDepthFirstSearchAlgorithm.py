import random
from src.algorithms.strategy.mazeGenerationStrategy import MazeGenerationStrategy
from src.maze.maze import Maze
from typing import Tuple, List

class DepthFirstSearch(MazeGenerationStrategy):
    """
    Maze generator using Depth-First Search witch backtracking.
    Algorithm overview:
    1. Start at a random cell and mark it as visited.
    2. While there are unvisited cells:
        a. Get all unvisited neighbours
        b. If unvisited neighbour exist:
            i. Randomly choose one
            ii. Make a path to it (mark intermediate cell as visited)
            iii. Push it onto stack
        c. If no unvisited neighbours:
            i. Backtrack by popping the stack
    """
    def __init__(self):
        self.cell = '1'
        self.wall = '0'
        self.stack = []

    def generate_maze(self, maze: Maze, on_step=None) -> None:
        self.on_step = on_step

        self.maze = maze

        # Choose one random starting position (ensuring it's not on the edge)
        self.start_height = random.randint(1, self.maze.height - 2)
        self.start_width = random.randint(1, self.maze.width - 2)
        self.start_cell = (self.start_height, self.start_width)

        # Marking starting cell as visited and begin processing
        self.maze.maze_matrix[self.start_cell] = self.cell
        self.animation()
        self.stack.append(self.start_cell)

        # Main generation loop
        while self.stack:
            current_cell = self.stack[-1]
            neightbors = self.get_unvisited_neighbors(current_cell)
            if neightbors:
                next_cell = random.choice(neightbors)
                self.stack.append(next_cell)
                self.make_path(current_cell, next_cell)
                self.maze.maze_matrix[next_cell] = self.cell
                self.animation()
            else:
                self.stack.pop()

    def get_unvisited_neighbors(self, current_cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Find all valid unvisited neighbors 2 cells away.
        """
        neighbors = []
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for direction in directions:
            neighbor = (current_cell[0] + direction[0], current_cell[1] + direction[1])
            if 0 < neighbor[0] < self.maze.height - 1 and 0 < neighbor[1] < self.maze.width - 1:
                if self.maze.maze_matrix[neighbor] == self.wall:
                    neighbors.append(neighbor)
        return neighbors

    def make_path(self, current_cell: Tuple[int, int], next_cell: Tuple[int, int]) -> None:
        """
        Creating a passage between two cells by marking the intermediate cell as visited.
        """
        path_cell = ((current_cell[0] + next_cell[0]) // 2, (current_cell[1] + next_cell[1]) // 2)
        self.maze.maze_matrix[path_cell] = self.cell

    def animation(self) -> None:
        """
        Triggers animation callback if provided.
        """
        if self.on_step:
            self.on_step(self.maze.maze_matrix)