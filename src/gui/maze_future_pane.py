import tkinter as tk
from tkinter import ttk

class FuturePanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Future feature").grid(row=0, column=0, columnspan=2, pady=5)
        self.export_maze_button = tk.Button(self, text="Export Maze")
        self.export_maze_button.grid(row=1, column=0, columnspan=2,  pady=5)

        self.export_maze_solution_button = tk.Button(self, text="Export Solution Maze")
        self.export_maze_solution_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.different_format = ttk.Combobox(self)
        self.different_format.grid(row=3, column=0, columnspan=2, pady=5)
