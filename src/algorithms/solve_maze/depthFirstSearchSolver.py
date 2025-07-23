from src.algorithms.strategy.mazeSolverStrategy import MazeSolverStrategy
from src.maze.maze import Maze

class DepthFirstSearchSolver(MazeSolverStrategy):
    """
    Solves mazes using DFS.
    """
    def solve_maze(self, maze: Maze, on_step=None) -> bool:
        if not maze.start or not maze.end:
            raise ValueError("Start and end positions must be set")

        self.on_step = on_step
        self.matrix = maze.maze_matrix

        start = maze.start
        end = maze.end

        stack = [start]
        visited = set()
        parent = {}

        while stack:
            position = stack.pop()
            x,y = position

            if position in visited:
                continue
            visited.add((x,y))

            # Marking visited
            if self.matrix[y][x] not in ('S', 'E'):
                self.matrix[y][x] = 'V'
            self.animation()

            # Path found
            if position == end:
                # Reconstructing the path
                while position != start:
                    x, y = position
                    if self.matrix[y][x] not in ('S','E'):
                        self.matrix[y][x] = "P"
                        self.animation()
                    position = parent[position]

                # Cleanup, reset visited nodes to paths
                for y in range(self.matrix.shape[0]):
                    for x in range(self.matrix.shape[1]):
                        if self.matrix[y][x] == 'V':
                            self.matrix[y][x] = '1'

                return True

            # Explore neighbors
            for dx, dy in [(-1,0), (1,0), (0, -1), (0, 1)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.matrix.shape[1] and 0 <= new_y < self.matrix.shape[0]:
                    if self.matrix[new_y][new_x] in ('1', 'E') and (new_x, new_y) not in visited:
                        parent[(new_x, new_y)] = (x, y)
                        stack.append((new_x, new_y))

        return False

    def animation(self) -> None:
        """
        Triggers animation callback.
        """
        if self.on_step:
            self.on_step(self.matrix)