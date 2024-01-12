from abc import ABC, abstractmethod

class MazeGenerationStrategy(ABC):
    @abstractmethod
    def generate_maze(self, maze):
        pass