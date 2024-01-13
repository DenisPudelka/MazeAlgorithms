import tkinter as tk
from .maze_canvas import MazeCanvas
from .new_south_panel import *
from src.algorithms.generate_maze.randomized_prims_algorithm import *
from src.algorithms.generate_maze.randomizes_depth_first_search_algorithm import *
from src.maze.maze import *


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Maze Application")
        self.geometry("650x700")

        self.maze_canvas = MazeCanvas(self)
        self.maze_canvas.pack(side="top", fill="both", expand=True)

        self.south_panel = SouthControlPanel(self, self.maze_canvas, self.generate_maze)
        self.south_panel.pack(side="bottom", fill="both")

        # self.north_panel.on_button_click(self.generate_and_display_maze)

    def generate_maze(self, width, height, algorithm):
        strategies = {
            'Randomized Prims': RandomizedPrimesAlgorithm,
            'Depth First Search': DepthFirstSearch
        }
        generation_strategy = strategies[algorithm]()
        self.maze = Maze(width, height, generation_strategy)
        self.maze.generate_maze()
        self.maze_canvas.update_maze(self.maze.maze_matrix)