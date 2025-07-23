import heapq
from src.algorithms.strategy.mazeSolverStrategy import MazeSolverStrategy
from src.maze.maze import Maze
from typing import Tuple, List


class AStarSearchSolver(MazeSolverStrategy):
    """
    Solves the maze using A* search.
    """
    def solve_maze(self, maze: Maze, on_step=None) -> bool:
        if not maze.start or not maze.end:
            raise ValueError("Start and end positions must be set")

        self.on_step = on_step
        self.matrix = maze.maze_matrix

        start = maze.start
        end = maze.end

        open_heap = []
        heapq.heappush(open_heap, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while open_heap:
            _, current = heapq.heappop(open_heap)
            x, y = current

            # Marking visited
            if self.matrix[y][x] not in ('S', 'E'):
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

            # Exploring neighbors
            for neighbor in self.neighbors(current):
                new_cost = cost_so_far[current] + 1 # Each step cost 1
                # If neighbor is new or cheaper to reach, update records
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(end, neighbor)
                    heapq.heappush(open_heap, (priority, neighbor))
                    came_from[neighbor] = current

        return False

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        """
        Manhattan distance heuristic between points a and b.
        """
        x1, y1 = a
        x2, y2 = b
        return abs(x1 - x2) + abs(y1 - y2)

    def neighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Returns walkable neighbors (up/down/left/right) of an node.
        """
        directions = [(0, 1), (1,0), (0,-1), (-1,0)]
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