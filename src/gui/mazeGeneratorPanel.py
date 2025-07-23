import tkinter as tk
from tkinter import ttk, messagebox

class MazeGeneratorPanel(tk.Frame):
    """
    Control panel for maze generation settings.
    """
    ALGORITHMS = (
        "Randomized Prims",
        "Depth First Search",
        "Kruskals Algorithm",
        "Wilson Algorithm",
        "Fractal Tessellation Algorithm",
        "Recursive Division"
    )
    DEFAULT_DIMENSION = 15

    def __init__(self, parent: tk.Widget, generate_callback) -> None:
        super().__init__(parent)
        self.generate_callback = generate_callback
        self.init_ui()


    def init_ui(self) -> None:
        """
        Initializing all UI components.
        """
        # Title
        tk.Label(self, text="Maze Generator").grid(row=0, column=0, columnspan=2, pady=5)

        # Dimensions
        tk.Label(self, text="Dimensions (MxM)").grid(row=1, column=0, pady=5)
        self.dimensions_entry = tk.Entry(self)
        self.dimensions_entry.grid(row=1, column=1, pady=5)
        self.dimensions_entry.insert(0, str(self.DEFAULT_DIMENSION))

        # Algorithm selection
        self.algorithm_combobox = ttk.Combobox(self)
        self.algorithm_combobox.grid(row=2, column=0, columnspan=10, pady=5)
        self.algorithm_combobox['values'] = self.ALGORITHMS
        self.algorithm_combobox['state'] = 'readonly'
        self.algorithm_combobox.current(0)

        # Animation Toggle
        self.var = tk.IntVar()
        self.check_button_animation = tk.Checkbutton(self, text="Animation")
        self.check_button_animation.grid(row=3, column=0, columnspan=3, pady=5)
        self.check_button_animation.config(variable=self.var, onvalue=1, offvalue=0, command=self.on_button_toggle)

        # Generate button
        self.generate_button = tk.Button(self, text="Generate")
        self.generate_button.grid(row=4, column=0, columnspan=2, pady=5)
        self.generate_button.config(command=self.generate_click)

    def on_button_toggle(self) -> bool:
        """
        Handle animation toggle changes.
        """
        if self.var.get() == 1:
            return True
        else:
            return False

    def generate_click(self) -> None:
        """
        Validate inputs and trigger maze generation.
        """
        try:
            dimension = int(self.dimensions_entry.get())
            if dimension <= 0:
                raise ValueError("Dimensions must be positive integers")

            self.generate_callback(
                width=dimension,
                height=dimension,
                algorithm=self.algorithm_combobox.get(),
                isAnimation=self.var.get()
            )
        except ValueError as e:
            self.errorMessage("Invalid Input", str(e))

    def errorMessage(self, title, message):
        """
        Display an error message.
        """
        messagebox.showerror(title=title, message=message)