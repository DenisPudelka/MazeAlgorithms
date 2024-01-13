import tkinter as tk
from .maze_canvas import MazeCanvas
from .north_control_panel import NorthControlPanel
from .south_controler_panel import SouthControlPanel
from src.maze.maze import Maze
from src.algorithms.generate_maze.randomizes_depth_first_search_algorithm import *
from src.algorithms.generate_maze.randomized_prims_algorithm import *


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Maze Application")
        self.geometry("800x600")

        self.maze_canvas = MazeCanvas(self)
        self.maze_canvas.pack(side="top", fill="both", expand=True)

        self.north_panel = NorthControlPanel(self)
        self.north_panel.pack(side="top", fill="x")

        self.south_panel = SouthControlPanel(self)
        self.south_panel.pack(side="bottom", fill="x")

        self.north_panel.on_button_click(self.generate_and_display_maze)

    def generate_and_display_maze(self):
        width, height = self.north_panel.get_dimensions()
        self.maze = Maze(width, height, RandomizedPrimesAlgorithm())
        self.maze.generate_maze()
        print(self.maze.maze_matrix)
        self.maze_canvas.update_maze(self.maze.maze_matrix)