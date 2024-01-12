from src.algorithms.generate_maze.randomized_prims_algorithm import *
import numpy as np

class Maze:
    # 0 - wall, 1 - walkable, S - start, E - end
    def __init__(self, width, height, generation_strategy, start=None, end=None):
        self.width = width
        self.height = height
        self.generation_strategy = generation_strategy
        self.maze_matrix = np.zeros((width, height), dtype='U1')
        self.maze_matrix[:] = '0'

        self.start = start if start else (0, 0)
        self.end = end if end else (height - 1, width - 1)

        self.maze_matrix[self.start] = 'S'
        self.maze_matrix[self.end] = 'E'

    def display_maze(self):
        print(self.maze_matrix)

    def generate_maze(self):
        generator = RandomizedPrimesAlgorithm(self)
        generator.generate_maze()
        #self.generation_strategy.generate_maze(self)

    def modify_maze(self, position, value):
        self.maze_matrix[position] = value
