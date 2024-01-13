import tkinter as tk
from tkinter import ttk
from .maze_generator_panel import *
from .maze_solver_panel import *
from .maze_future_pane import *

class SouthControlPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.generator_panel = MazeGeneratorPanel(self)
        self.generator_panel.grid(row=0, column=0, padx=25, pady=5)

        self.solver_panel = MazeSolverPanel(self)
        self.solver_panel.grid(row=0, column=1, padx=25, pady=5)

        self.future_panel = FuturePanel(self)
        self.future_panel.grid(row=0, column=2, padx=25, pady=5)

