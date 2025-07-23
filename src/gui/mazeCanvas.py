import tkinter as tk
from typing import Optional
import numpy as np

class MazeCanvas(tk.Canvas):
    """
    A custom Canvas widget for displaying and interacting with maze.
    """
    COLOR_WALL = "black"
    COLOR_PATH = "white"
    COLOR_START = "blue"
    COLOR_END = "green"
    COLOR_VISITED = "PaleGreen2"
    COLOR_SOLUTION = "yellow"
    COLOR_BACKGROUND = "blue"

    def __init__(self, parent: tk.Widget, maze: Optional[np.ndarray] =None,
                 width: int =400, height: int =400, **kwargs) -> None:
        super().__init__(parent, width=width, height=height, **kwargs, background=self.COLOR_BACKGROUND)
        self.maze = maze
        self.cell_width = None
        self.cell_height = None
        if maze is not None:
            self.draw_maze()
        self.bind("<Configure>", self.on_resize)

    def draw_maze(self) -> None:
        """
        Redraw the entire maze based on current dimensions.
        """
        if self.maze is None:
            return

        self.delete('all')
        rows, cols = self.maze.shape
        self.cell_width = self.winfo_width() / cols
        self.cell_height = self.winfo_height() / rows

        for y in range(rows):
            for x in range(cols):
                self.draw_cell(x, y)

    def draw_cell(self, x: int, y: int) -> None:
        """
        Draw single cell at (x, y).
        """
        x1 = x * self.cell_width
        y1 = y * self.cell_height
        x2 = x1 + self.cell_width
        y2 = y1 + self.cell_height
        cell_value = self.maze[y][x]
        color = {
            "0": self.COLOR_WALL,
            "1": self.COLOR_PATH,
            "S": self.COLOR_START,
            "E": self.COLOR_END,
            "P": self.COLOR_SOLUTION,
            "V": self.COLOR_VISITED
        }.get(cell_value, self.COLOR_WALL)

        self.create_rectangle(x1, y1, x2, y2, fill=color)

    def update_maze(self, maze_matrix):
        """
        Update the displayed maze with new data.
        """
        self.maze = maze_matrix
        self.draw_maze()

    def on_resize(self, event):
        """
        Handle canvas resize events.
        """
        if self.maze is None:
            return
        self.cell_width = event.width / len(self.maze[0])
        self.cell_height = event.height / len(self.maze)
        self.draw_maze()

    def enable_click_selection(self, callback):
        """
        Enable clicking on maze cells to trigger callback.
        """
        self.bind("<Button-1>", lambda event: self.on_canvas_click(event, callback))

    def on_canvas_click(self, event, callback):
        """
        Converting click coordinates to maze cell indices.
        """
        if self.cell_width is None or self.cell_height is None:
            return

        x = int(event.x // self.cell_width)
        y = int(event.y // self.cell_height)

        if 0 <= x < self.maze.shape[1] and 0 <= y < self.maze.shape[0]:
            callback((x, y))