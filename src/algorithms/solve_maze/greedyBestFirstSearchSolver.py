import heapq
from src.maze.maze import Maze
from src.algorithms.strategy.mazeSolverStrategy import MazeSolverStrategy
from typing import Tuple, List

class GreedyBestFirstSearchSolver(MazeSolverStrategy):
    """
    Solves mazes using Greedy Best-First Search.
    """
    def solve_maze(self, maze: Maze, on_step=None) -> bool:
        if not maze.start or not maze.end:
            raise ValueError("Start and end positions must be set")

        self.on_step = on_step
        self.matrix = maze.maze_matrix

        start = maze.start
        end = maze.end

        open_list = []
        heapq.heappush(open_list, (self.heuristic(start, end), start))
        came_from = {start: None}
        visited = set()

        while open_list:
            _, current = heapq.heappop(open_list)
            x, y = current

            if current in visited:
                continue
            visited.add(current)

            # Marking visited
            if current != start and current != end:
                self.matrix[y][x] = 'V'
            self.animation()

            # Path found
            if current == end:
                # Reconstructing the path
                while current != start:
                    x, y = current
                    if self.matrix[y][x] not in ('S', 'E'):
                        self.matrix[y][x] = 'P'
                        self.animation()
                    current = came_from[current]

                # Cleanup, reset visited nodes to paths
                for y in range(self.matrix.shape[0]):
                    for x in range(self.matrix.shape[1]):
                        if self.matrix[y][x] == 'V':
                            self.matrix[y][x] = '1'
                return True

            # Explore neighbors
            for neighbor in self.neighbors(current):
                if neighbor not in visited:
                    came_from[neighbor] = current
                    priority = self.heuristic(neighbor, end)
                    heapq.heappush(open_list, (priority, neighbor))

        return False

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        """
        Manhattan distance between two points.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Returns walkable adjacent cells.
        """
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        result = []
        for dx, dy in directions:
            nx, ny = node[0] + dx, node[1] + dy
            if (0 <= nx < self.matrix.shape[1] and
                0 <= ny < self.matrix.shape[0] and
                self.matrix[ny][nx] != '0'):
                result.append((nx, ny))
        return result

    def animation(self) -> None:
        """
        Triggers animation callback.
        """
        if self.on_step:
            self.on_step(self.matrix)