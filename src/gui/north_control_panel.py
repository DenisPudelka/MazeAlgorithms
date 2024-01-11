import tkinter as tk
from tkinter import ttk

class NorthControlPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_widgets()


    def create_widgets(self):
        # Label for width input
        self.width_label = ttk.Label(self, text="Width:")
        self.width_label.grid(row=0, column=0, padx=5, pady=5)

        # Entry for width
        self.width_entry = ttk.Entry(self)
        self.width_entry.grid(row=0, column=1, padx=5, pady=5)

        # Label for height input
        self.height_label = ttk.Label(self, text="Height:")
        self.height_label.grid(row=1, column=0, padx=5, pady=5)

        # Entry for height
        self.height_entry = ttk.Entry(self)
        self.height_entry.grid(row=1, column=1, padx=5, pady=5)

        # Button
        self.button = ttk.Button(self, text="Generate Maze", command=self.generate_maze)
        self.button.grid(row=2, column=0, columnspan=2, pady=5)


    def generate_maze(self):
        width = self.width_entry.get()
        height = self.height_entry.get()
        print("Width: " , width , " Height: " , height )
