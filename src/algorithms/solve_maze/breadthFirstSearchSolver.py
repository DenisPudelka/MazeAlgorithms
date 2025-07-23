from collections import deque
from src.maze.maze import Maze
from src.algorithms.strategy.mazeSolverStrategy import MazeSolverStrategy

class BreadthFirstSearchSolver(MazeSolverStrategy):
    """
    Uses BFS to solve the maze.
    """
    def solve_maze(self, maze: Maze, on_step=None) -> bool:
        if not maze.start or not maze.end:
            raise ValueError("Start and end positions must be set")

        self.on_step = on_step
        self.matrix = maze.maze_matrix

        start = maze.start
        end = maze.end

        queue = deque([start])
        visited = set()
        parent = {}
        visited.add(start)

        while queue:
            current = queue.popleft()
            x,y = current

            # Marking visited
            if self.matrix[y][x] not in ('S', 'E'):
                self.matrix[y][x] = 'V'
            self.animation()

            # Path found
            if current == end:
                # Reconstructing the path
                while current != start:
                    x,y = current
                    if self.matrix[y][x] not in ('S', 'E'):
                        self.matrix[y][x] = 'P'
                        self.animation()
                    current = parent[current]

                # Cleanup, reset visited nodes to paths
                for y in range(self.matrix.shape[0]):
                    for x in range(self.matrix.shape[1]):
                        if self.matrix[y][x] == 'V':
                            self.matrix[y][x] = '1'

                return True

            # Exploring neighbors
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                new_x, new_y = x + dx, y + dy
                next_cell = (new_x, new_y)
                if (0 <= new_x < self.matrix.shape[1] and 0 <= new_y < self.matrix.shape[0]
                    and self.matrix[new_y][new_x] in ('1','E') and next_cell not in visited):
                    parent[next_cell] = current
                    queue.append(next_cell)
                    visited.add(next_cell)

        return False

    def animation(self) -> None:
        """
        Triggers animation callback.
        """
        if self.on_step:
            self.on_step(self.matrix)