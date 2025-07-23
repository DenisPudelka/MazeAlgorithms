import heapq
from src.maze.maze import Maze
from src.algorithms.strategy.mazeSolverStrategy import MazeSolverStrategy
from typing import List, Tuple

class DijkstraSolver(MazeSolverStrategy):
    """
    Solves mazes using Dijkstra's algorithm.
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
            current_cost, current = heapq.heappop(open_heap)
            x, y = current

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
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(open_heap, (new_cost, neighbor))
                    came_from[neighbor] = current

        return False


    def neighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Returns walkable adjacent cells (up/down/left/right).
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