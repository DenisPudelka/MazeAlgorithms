from abc import ABC, abstractmethod

class MazeSolverStrategy(ABC):
    @abstractmethod
    def solve_maze(self, maze, on_step=None):
        pass

    @abstractmethod
    def animation(self):
        pass