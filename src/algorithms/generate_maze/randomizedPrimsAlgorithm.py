import random
from src.algorithms.strategy.mazeGenerationStrategy import MazeGenerationStrategy

class RandomizedPrimesAlgorithm(MazeGenerationStrategy):
    """
    Implementation of the Randomized Prim's algorithm for maze generation.
    The algorithm works by:
        1. Starting with a grid full of walls ('0')
        2. Picking a starting cell and making it as part of the maze ('1')
        3. Adding the walls of the starting cell to the wall list
        4. While there are walls in the list:
            a. Pick a random wall from the list
            b. If only one of the two cells divided by the wall is visited:
                i. Make the wall a passage ('1')
                ii. Add the neighbouring walls of the newly visited cell to the wall list
            c. Remove the wall from the list
    """
    def __init__(self):
        self.unvisited = '0'
        self.cell = '1'
        self.maze = None
        self.start_cell = None


    def generate_maze(self, maze, on_step=None):
        self.on_step = on_step

        self.maze = maze

        # Initializing all cells as unvisited
        self.maze.maze_matrix[:] = self.unvisited

        # Setting starting position
        self.start_cell = (maze.start[0], maze.start[1])
        self.maze.maze_matrix[self.start_cell] = self.cell
        self.animation()

        # Initializing wall list with staring cell's neighbours
        wall_list = self.get_init_walls()

        while wall_list:
            rand_wall = random.choice(wall_list)
            y, x = rand_wall

            # up
            if y <= self.maze.height - 2:
                if self.maze.maze_matrix[y + 1][x] == self.unvisited and \
                        self.maze.maze_matrix[y - 1][x] == self.cell:
                    surrounding_cells = self.surrounding_cells(rand_wall)
                    if surrounding_cells < 2:
                        self.maze.maze_matrix[y][x] = self.cell
                        self.update_walls(wall_list, y, x)
                        self.delete_wall(wall_list, rand_wall)
                        self.animation()
                        continue

            # down
            if y > 0:
                if self.maze.maze_matrix[y - 1][x] == self.unvisited and \
                        self.maze.maze_matrix[y + 1][x] == self.cell:
                    surrounding_cells = self.surrounding_cells(rand_wall)
                    if surrounding_cells < 2:
                        self.maze.maze_matrix[y][x] = self.cell
                        self.update_walls(wall_list, y, x)
                        self.delete_wall(wall_list, rand_wall)
                        self.animation()
                        continue

            # left
            if x > 0:
                if self.maze.maze_matrix[y][x - 1] == self.unvisited and \
                        self.maze.maze_matrix[y][x + 1] == self.cell:
                    surrounding_cells = self.surrounding_cells(rand_wall)
                    if surrounding_cells < 2:
                        self.maze.maze_matrix[y][x] = self.cell
                        self.update_walls(wall_list, y, x)
                        self.delete_wall(wall_list, rand_wall)
                        self.animation()
                        continue

            # right
            if x <= self.maze.width - 2:
                if self.maze.maze_matrix[y][x + 1] == self.unvisited and \
                        self.maze.maze_matrix[y][x - 1] == self.cell:
                    surrounding_cells = self.surrounding_cells(rand_wall)
                    if surrounding_cells < 2:
                        self.maze.maze_matrix[y][x] = self.cell
                        self.update_walls(wall_list, y, x)
                        self.delete_wall(wall_list, rand_wall)
                        self.animation()
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

    def animation(self):
        if self.on_step:
            self.on_step(self.maze.maze_matrix)