import tkinter as tk
from .maze_canvas import MazeCanvas
from .north_control_panel import NorthControlPanel
from .south_controler_panel import SouthControlPanel

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

