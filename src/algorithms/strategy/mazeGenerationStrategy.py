from abc import ABC, abstractmethod

class MazeGenerationStrategy(ABC):
    @abstractmethod
    def generate_maze(self, maze, on_step=None):
        pass

    @abstractmethod
    def animation(self):
        pass