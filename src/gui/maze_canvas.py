import tkinter as tk

class MazeCanvas(tk.Canvas):
    def __init__(self, parent, maze=None, width=400, height=400, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs, background="blue")
        self.maze = maze
        self.cell_width = None
        self.cell_height = None
        if maze:
            self.draw_maze()
        self.bind("<Configure>", self.on_resize)

    def draw_maze(self):
        if self.maze is None:
            return

        self.delete('all')
        rows, cols = len(self.maze), len(self.maze[0])
        self.cell_width = self.winfo_width() / cols
        self.cell_height = self.winfo_height() / rows

        for y in range(rows):
            for x in range(cols):
                x1 = x * self.cell_width
                y1 = y * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height
                if self.maze[y][x] == '1':
                    self.create_rectangle(x1, y1, x2, y2, fill="white")
                else:
                    self.create_rectangle(x1, y1, x2, y2, fill="black")

    def update_maze(self, maze_matrix):
        self.maze = maze_matrix
        self.draw_maze()

    def on_resize(self, event):
        if self.maze is None:
            return
        self.cell_width = event.width / len(self.maze[0])
        self.cell_height = event.height / len(self.maze)
        self.draw_maze()
