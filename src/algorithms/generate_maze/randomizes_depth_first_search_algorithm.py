import numpy as np
import queue as q
import random
from strategy.maze_generation_strategy import *

class DepthFirstSearch(MazeGenerationStrategy):
    def __init__(self, maze):
        self.cell = '1'
        self.unvisited = '0'
        self.queue = q.Queue

    def generate_maze(self, maze):
        # Initialization of DFS
        self.maze = maze
        self.start_height = random.randint(1, self.maze.height - 2)
        self.start_width = random.randint(1, self.maze.width - 2)
        self.start_cell = (self.start_height, self.start_width)
        self.maze.maze_matrix[self.start_cell] = self.cell
        self.queue.put(self.start_cell)

        # Implementation of DFS