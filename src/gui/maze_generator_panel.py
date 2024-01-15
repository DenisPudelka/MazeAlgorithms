import tkinter as tk
from tkinter import ttk


class MazeGeneratorPanel(tk.Frame):
    def __init__(self, parent, generate_callback):
        super().__init__(parent)
        self.generate_callback = generate_callback

        tk.Label(self, text="Maze Generator").grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(self, text="Width").grid(row=1, column=0, pady=5)
        self.width_entry = tk.Entry(self)
        self.width_entry.grid(row=1, column=1, pady=5)
        tk.Label(self, text="Height").grid(row=2, column=0, pady=5)
        self.height_entry = tk.Entry(self)
        self.height_entry.grid(row=2, column=1, pady=5)

        self.algorithm_combobox = ttk.Combobox(self)
        self.algorithm_combobox.grid(row=3, column=0, columnspan=2, pady=5)
        self.algorithm_combobox['values'] = ('Randomized Prims', 'Depth First Search', 'Kruskals Algorithm')
        self.algorithm_combobox['state'] = 'readonly'
        self.algorithm_combobox.current(0)

        self.generate_button = tk.Button(self, text="Generate")
        self.generate_button.grid(row=4, column=0, columnspan=2, pady=5)
        self.generate_button.config(command=self.generate_click)

    def generate_click(self):
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            algorithm = self.algorithm_combobox.get()

            self.generate_callback(width, height, algorithm)
        except ValueError:
            print("Please enter valid numbers for width and height.")

