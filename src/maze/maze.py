import numpy as np

class Maze:
    # 0 - wall, 1 - walkable, S - start, E - end
    def __init__(self, width, height, start=None, end=None):
        self.width = width
        self.height = height
        self.maze_matrix = np.zeros((width, height), dtype='U1')
        self.maze_matrix[:] = '0'

        self.start = start if start else (0, 0)
        self.end = end if end else (height - 1, width - 1)

        self.maze_matrix[self.start] = 'S'
        self.maze_matrix[self.end] = 'E'

    def display_maze(self):
        print(self.maze_matrix)

    def generate_maze(self):
        pass

    def modify_maze(self, position, value):
        self.maze_matrix[position] = value
