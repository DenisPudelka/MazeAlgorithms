import tkinter as tk
from tkinter import ttk, messagebox
from typing import Tuple

class MazeSolverPanel(tk.Frame):
    """
    Control panel for maze solving settings.
    """
    ALGORITHMS = (
        "DepthFirstSearch",
        "BreadthFirstSearch",
        "A*",
        "Dijkstra",
        "GreedyBestFirstSearch"
    )

    def __init__(self, parent: tk.Widget, canvas, solve_callback, app) -> None:
        super().__init__(parent)
        self.app = app
        self.canvas = canvas
        self.solve_callback = solve_callback
        self.init_ui()

    def init_ui(self) -> None:
        # Title
        tk.Label(self, text="Solve Maze").grid(row=0, column=0, columnspan=2, pady=5)

        # Start/End selection
        self.start_label = tk.Label(self, text="Start: Not picked")
        self.start_label.grid(row=1, column=0)
        self.end_label = tk.Label(self, text="End: Not picked")
        self.end_label.grid(row=2, column=0)
        tk.Button(self, text="Pick Start", command=self.pick_start).grid(row=1, column=1)
        tk.Button(self, text="Pick End", command=self.pick_end).grid(row=2, column=1)

        # Algorithm selection
        self.algorithm_combobox = ttk.Combobox(self)
        self.algorithm_combobox.grid(row=3, column=0, columnspan=2, pady=5)
        self.algorithm_combobox['values'] = self.ALGORITHMS
        self.algorithm_combobox['state'] = 'readonly'
        self.algorithm_combobox.current(0)

        # Animation toggle
        self.var = tk.IntVar()
        self.check_button_animation = tk.Checkbutton(self, text="Animation")
        self.check_button_animation.grid(row=4, column=0, columnspan=3, pady=5)
        self.check_button_animation.config(variable=self.var, onvalue=1, offvalue=0, command=self.on_button_toggle)

        # Solve button
        self.solve_button = tk.Button(self, text="Solve")
        self.solve_button.grid(row=4, column=1, columnspan=2, pady=5)
        self.solve_button.config(command=self.solve_click)

    def pick_start(self) -> None:
        """
        Enable start point selection.
        """
        self.app.pick_mode = "start"
        self.canvas.enable_click_selection(self.app.on_tile_clicked)

    def pick_end(self) -> None:
        """
        Enable end point selection.
        """
        self.app.pick_mode = "end"
        self.canvas.enable_click_selection(self.app.on_tile_clicked)

    def update_start_label(self, pos: Tuple[int, int]) -> None:
        self.start_label.config(text=f"Start: {pos}")

    def update_end_label(self, pos: Tuple[int, int]) -> None:
        self.end_label.config(text=f"End: {pos}")

    def on_button_toggle(self) -> bool:
        """
        Handle animation toggle changes.
        """
        if self.var.get() == 1:
            return True
        else:
            return False

    def solve_click(self) -> None:
        """
        Validate inputs and trigger maze solving.
        """
        if not self.app.maze.start or not self.app.maze.end:
            self.errorMessage("Error", "Set start and end points first")
            return
        try:
            self.solve_callback(
                algorithm=self.algorithm_combobox.get(),
                isAnimation=self.var.get()
            )
        except ValueError as e:
            self.errorMessage("Error", str(e))

    def errorMessage(self, title: str, message: str) -> None:
        """
        Display an error message.
        """
        messagebox.showerror(title=title, message=message)