import tkinter as tk
from tkinter import ttk

class MazeGeneratorPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Maze Generator").grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(self, text="Width").grid(row=1, column=0, pady=5)
        self.width_entry = tk.Entry(self)
        self.width_entry.grid(row=1, column=1, pady=5)
        tk.Label(self, text="Height").grid(row=2, column=0, pady=5)
        self.height_entry = tk.Entry(self)
        self.height_entry.grid(row=2, column=1, pady=5)

        self.algorithm_combobox = ttk.Combobox(self)
        self.algorithm_combobox.grid(row=3, column=0, columnspan=2, pady=5)

        self.generate_button = tk.Button(self, text="Generate")
        self.generate_button.grid(row=4, column=0, columnspan=2, pady=5)