import numpy as np
import random
from src.algorithms.generate_maze.strategy.maze_generation_strategy import MazeGenerationStrategy

class RandomizedPrimesAlgorithm(MazeGenerationStrategy):
    def __init__(self):
        self.unvisited = '0'
        self.cell = '1'


    def generate_maze(self, maze):
        self.maze = maze
        self.maze.maze_matrix[:] = self.unvisited
        self.start_height = random.randint(1, maze.height - 2)  # making sure we dont start/end on edge
        self.start_width = random.randint(1, maze.width - 2)  # making sure we dont start/end on edge
        self.start_cell = (self.start_height, self.start_width)  # making sure we dont start/end on edge
        self.maze.maze_matrix[self.start_cell] = self.cell  # starting cell

        wall_list = self.get_init_walls()
        while wall_list:
            rand_wall = random.choice(wall_list)
            y, x = rand_wall

            # up
            if y <= self.maze.height - 2:
                if self.maze.maze_matrix[y + 1][x] == self.unvisited and \
                        self.maze.maze_matrix[y - 1][x] == self.cell:  # up U
                    surrounding_cells = self.surrounding_cells(rand_wall)
                    if surrounding_cells < 2:
                        self.maze.maze_matrix[y][x] = self.cell
                        self.update_walls(wall_list, y, x)
                        self.delete_wall(wall_list, rand_wall)
                        continue

            # down
            if y > 0:
                if self.maze.maze_matrix[y - 1][x] == self.unvisited and \
                        self.maze.maze_matrix[y + 1][x] == self.cell:  # down u
                    surrounding_cells = self.surrounding_cells(rand_wall)
                    if surrounding_cells < 2:
                        self.maze.maze_matrix[y][x] = self.cell
                        self.update_walls(wall_list, y, x)
                        self.delete_wall(wall_list, rand_wall)
                        continue

            # left
            if x > 0:
                if self.maze.maze_matrix[y][x - 1] == self.unvisited and \
                        self.maze.maze_matrix[y][x + 1] == self.cell:  # left U
                    surrounding_cells = self.surrounding_cells(rand_wall)
                    if surrounding_cells < 2:
                        self.maze.maze_matrix[y][x] = self.cell
                        self.update_walls(wall_list, y, x)
                        self.delete_wall(wall_list, rand_wall)
                        continue

            if x <= self.maze.width - 2:
                if self.maze.maze_matrix[y][x + 1] == self.unvisited and \
                        self.maze.maze_matrix[y][x - 1] == self.cell:  # right U
                    surrounding_cells = self.surrounding_cells(rand_wall)
                    if surrounding_cells < 2:
                        self.maze.maze_matrix[y][x] = self.cell
                        self.update_walls(wall_list, y, x)
                        self.delete_wall(wall_list, rand_wall)
                        continue

            self.delete_wall(wall_list, rand_wall)

    def get_init_walls(self):
        y, x = self.start_cell
        walls = []

        walls.append([y + 1, x])  # down
        walls.append([y - 1, x])  # up
        walls.append([y, x + 1])  # left
        walls.append([y, x - 1])  # right

        return walls

    def surrounding_cells(self, wall):
        s_cells = 0
        y, x = wall

        if 0 < y < self.maze.height - 1 and self.maze.maze_matrix[y - 1][x] == self.cell:
            s_cells += 1
        if 0 < y < self.maze.height - 1 and self.maze.maze_matrix[y + 1][x] == self.cell:
            s_cells += 1
        if 0 < x < self.maze.width - 1 and self.maze.maze_matrix[y][x + 1] == self.cell:
            s_cells += 1
        if 0 < x < self.maze.width - 1 and self.maze.maze_matrix[y][x - 1] == self.cell:
            s_cells += 1

        return s_cells

    def delete_wall(self, walls, rand_wall):
        walls.remove(rand_wall)

    def update_walls(self, wall_list, y, x):
        if 0 < y + 1 < self.maze.height - 1 and [y + 1, x] not in wall_list:
            wall_list.append([y + 1, x])
        if 0 < y - 1 < self.maze.height - 1 and [y - 1, x] not in wall_list:
            wall_list.append([y - 1, x])
        if 0 < x + 1 < self.maze.width - 1 and [y, x + 1] not in wall_list:
            wall_list.append([y, x + 1])
        if 0 < x - 1 < self.maze.width - 1 and [y, x - 1] not in wall_list:
            wall_list.append([y, x - 1])