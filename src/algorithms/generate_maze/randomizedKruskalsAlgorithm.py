import random
from src.algorithms.strategy.mazeGenerationStrategy import MazeGenerationStrategy
from .utils.disjointSet import DisjointSet
from src.maze.maze import Maze

class RandomizedKruskalAlgorith(MazeGenerationStrategy):
    """
    Implementation of Kruskal's algorithm for maze generation with random wall selection.
    Creates a maze by treating walls as potential connections between cells.
    Uses a disjoint-set (Union-Find) data structure to avoid cycles.
    """
    def __init__(self):
        self.cell = "1"
        self.wall = "0"

    def generate_maze(self, maze: Maze, on_step=None) -> None:
        self.on_step = on_step
        width, height = maze.width, maze.height
        self.maze = maze
        self.maze.maze_matrix[:] = self.wall

        # Calculates grid dimensions for cell positions (ignoring borders)
        cell_width = (width - 1) // 2
        cell_hight = (height - 1) // 2

        # Initialize Disjoint-Set to track connected cells
        ds = DisjointSet(cell_width * cell_hight)

        # List to store all removable walls
        walls = []

        # Add vertical walls (between cells horizontally)
        for y in range(1, height - 1, 2):
            for x in range(2, width - 1, 2):
                walls.append((x, y))

        # Add horizontal walls (between cells vertically)
        for y in range(2, height - 1, 2):
            for x in range(1, width - 1, 2):
                walls.append((x, y))

        # Randomizing wall processing order
        random.shuffle(walls)

        # Processing each wall in random order
        for wall in walls:
            x, y = wall

            if x % 2 == 0:  # Vertical wall
                # Cells on either side of the vertical wall
                cell1_x = (x - 1) // 2
                cell1_y = (y - 1) // 2
                cell2_x = (x + 1) // 2
                cell2_y = (y - 1) // 2
            else:  # Horizontal wall
                # Cells on either side of the horizontal wall
                cell1_x = (x - 1) // 2
                cell1_y = (y - 1) // 2
                cell2_x = (x - 1) // 2
                cell2_y = (y + 1) // 2

            # Convert 2D cell coordinates to 1D index
            cell1 = cell1_y * cell_width + cell1_x
            cell2 = cell2_y * cell_width + cell2_x

            if ds.find(cell1) != ds.find(cell2):
                # Remove the wall
                self.maze.modify_maze((x, y), self.cell)
                self.animation()
                # Connect the cells
                ds.union(cell1, cell2)

        # Set all cell positions (odd coordinates) to be walkable
        for y in range(1, height - 1, 2):
            for x in range(1, width - 1, 2):
                self.maze.modify_maze((x, y), self.cell)
                self.animation()

    def animation(self) -> None:
        """
        Triggers animation callback if provided.
        """
        if self.on_step:
            self.on_step(self.maze.maze_matrix)