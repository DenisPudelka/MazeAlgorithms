import numpy as np
import random
from src.algorithms.generate_maze.strategy.maze_generation_strategy import MazeGenerationStrategy


class DepthFirstSearch(MazeGenerationStrategy):
    def __init__(self):
        self.cell = '1'
        self.wall = '0'
        self.stack = []

    def generate_maze(self, maze):
        # Initialization of DFS
        self.maze = maze
        self.start_height = random.randint(1, self.maze.height - 2)
        self.start_width = random.randint(1, self.maze.width - 2)
        self.start_cell = (self.start_height, self.start_width)
        # self.start_cell = (1, 1)
        self.maze.maze_matrix[self.start_cell] = self.cell
        self.stack.append(self.start_cell)

        # Implementation of DFS
        while self.stack:
            current_cell = self.stack[-1]
            neightbors = self.get_unvisited_neighbors(current_cell)
            if neightbors:
                next_cell = random.choice(neightbors)
                self.stack.append(next_cell)
                self.make_path(current_cell, next_cell)
                self.maze.maze_matrix[next_cell] = self.cell
            else:
                self.stack.pop()

    def get_unvisited_neighbors(self, current_cell):
        neighbors = []
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for direction in directions:
            neighbor = (current_cell[0] + direction[0], current_cell[1] + direction[1])
            if 0 < neighbor[0] < self.maze.height - 1 and 0 < neighbor[1] < self.maze.width - 1:
                if self.maze.maze_matrix[neighbor] == self.wall:
                    neighbors.append(neighbor)
        return neighbors

    def make_path(self, current_cell, next_cell):
        path_cell = ((current_cell[0] + next_cell[0]) // 2, (current_cell[1] + next_cell[1]) // 2)
        self.maze.maze_matrix[path_cell] = self.cell
