import random
from src.maze.maze import Maze
from src.algorithms.strategy.mazeGenerationStrategy import MazeGenerationStrategy

class FractalTessellationAlgorithm(MazeGenerationStrategy):
    """
    A class that implements a Fractal Tessellation-based algorithm for maze generation.
    This algorithm recursively tiles the maze with base patterns, forming a fractal-like structure.
    1. Place base block to each region (A, B, C, D)
    2. Create 3 passages between 4 possible connections (AB, AC, BD, CD)
    3. Expand recursively newly created base block.
    """
    def __init__(self):
        self.cell = '1'
        self.wall = '0'

    def generate_maze(self, maze: Maze, on_step=None) -> None:
        """
        Generates the maze using fractal tessellation algorithm.
        """
        self.on_step = on_step
        self.maze = maze

        self.width = self.maze.width
        self.height = self.maze.height

        # Fill the maze with paths (empty maze)
        for y in range(self.width):
            for x in range(self.height):
                self.maze.maze_matrix[y][x] = '1'

        # Base 3x3 block pattern: walls in every position except center
        base = [
            (0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)
        ]

        # Initial size of block pattern (3x3)
        current_height = (len(base)//2)-1
        current_width = (len(base)//2)-1

        # Expand blocks while fitting within maze bounds
        while current_height * 2 <= self.height and current_width * 2 <= self.width:
            # Positions of 4 sub-blocks
            positions = [
                (0, 0), # A - block
                (0, current_width-1), # B - block
                (current_height-1, 0), # C - block
                (current_height-1, current_width-1) # D - block
            ]

            # Carve each base pattern into the maze
            for position in positions:
                y, x = position
                for tmp in base:
                    ny, nx = tmp[0] + y, tmp[1] + x
                    self.maze.maze_matrix[ny][nx] = '0'
                    self.animation()

            # Double the current block size for next level
            current_height += current_height
            current_width += current_width

            # Shuffle and apply 3 out of 4 wall connections between adjacent blocks
            connections = ['AB', 'AC', 'BD', 'CD']
            random.shuffle(connections)
            used_walls = set()
            middle_y = (current_height - 1) // 2
            middle_x = (current_width - 1) // 2

            wall_candidates = {
                'AB': [(y, middle_x) for y in range(1, middle_y)],
                'AC': [(middle_y, x) for x in range(1, middle_x)],
                'BD': [(middle_y, x) for x in range(middle_x+1, current_width-2)],
                'CD': [(y, middle_x) for y in range(middle_y+1, current_height-2)],
            }

            for conn in connections[:3]:
                walls = wall_candidates[conn]
                random.shuffle(walls)
                for wy, wx in walls:
                    if self.is_valid_wall(wy, wx):
                        self.maze.maze_matrix[wy][wx] = '1'
                        self.animation()
                        used_walls.add((wy, wx))
                        break

            # Recalculate the base for next level (only keep walls)
            base = [
                (y, x) for y in range(current_height-1)
                for x in range(current_width-1)
                if self.maze.maze_matrix[y][x] == '0'
            ]

            current_height -= 1
            current_width -= 1

    def is_valid_wall(self, y: int, x: int) -> bool:
        """
        Checks if placing a connection wall at (y, x) is valid.
        A wall is valid if it's currently a wall cell ('0') and it connects
        to exactly two path cells either horizontally or vertically.
        """
        if self.maze.maze_matrix[y][x] != '0':
            return False

        # Check bounds and values
        top = y > 0 and self.maze.maze_matrix[y - 1][x] == '1'
        bottom = y < self.height - 1 and self.maze.maze_matrix[y + 1][x] == '1'
        left = x > 0 and self.maze.maze_matrix[y][x - 1] == '1'
        right = x < self.width - 1 and self.maze.maze_matrix[y][x + 1] == '1'

        return (top and bottom) or (left and right)

    def animation(self) -> None:
        """
        Triggers animation callback if provided.
        """
        if self.on_step:
            self.on_step(self.maze.maze_matrix)