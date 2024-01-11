import tkinter as tk
from tkinter import ttk

class SouthControlPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_widgets()


    def create_widgets(self):
        # Label for different maze generator alg
        self.generate_maze_label = ttk.Label(self, text="Maze generator")
        self.generate_maze_label.grid(row=0, column=0, padx=5, pady=5)

        # Combobox for maze generator
        self.selected_generator = tk.StringVar()
        self.generator_cb = ttk.Combobox(self, textvariable=self.selected_generator)
        self.generator_cb['values'] = ['Generator 1', 'Generator 2', 'Generator 3']
        self.generator_cb['state'] = 'readonly'
        self.generator_cb.grid(row=1, column=0, padx=5, pady=5)

        # Button for generator
        self.generator_button = ttk.Button(self, text="Generate Maze", command=self.generate_maze)
        self.generator_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Label for different maze solver algorithms
        self.solve_maze_label = ttk.Label(self, text="Maze solver")
        self.solve_maze_label.grid(row=0, column=1, padx=5, pady=5)  # Adjust the row/column as needed

        # Combobox for maze solver
        self.selected_solver = tk.StringVar()
        self.solver_cb = ttk.Combobox(self, textvariable=self.selected_solver)
        self.solver_cb['values'] = ['Solver 1', 'Solver 2', 'Solver 3']  # Update with actual solver names
        self.solver_cb['state'] = 'readonly'  # Ensures that the user can only select from the list
        self.solver_cb.grid(row=1, column=1, padx=5, pady=5)

        # Button for solver
        self.solver_button = ttk.Button(self, text="Solve Maze", command=self.solve_maze)
        self.solver_button.grid(row=2, column=1, columnspan=2, pady=5)


    def generate_maze(self):
        selected_generator = self.selected_generator.get()
        print(f"Generating maze using {selected_generator} algorithm")

    def solve_maze(self):
        selected_solver = self.selected_solver.get()
        print(f"Solving maze using {selected_solver} algorithm")