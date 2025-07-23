from .mazeCanvas import MazeCanvas
from .mazeGeneratorPanel import *
from .mazeSolverPanel import *

class SouthControlPanel(tk.Frame):
    """
    A container frame for maze generator and solver control panels.
    """
    def __init__(self, parent: tk.Widget, maze_canvas, generate_callback, solve_callback, app) -> None:
        super().__init__(parent)
        self._validate_inputs(maze_canvas, generate_callback, solve_callback)

        self.canvas = maze_canvas
        self.app = app

        self.configure(borderwidth=1, relief="solid")
        self.init_ui(generate_callback, solve_callback)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.pack_propagate(False)

    def init_ui(self, generate_callback, solve_callback) -> None:
        """
        Initializing child panels.
        """
        self.generator_panel = MazeGeneratorPanel(self, generate_callback)
        self.generator_panel.grid(row=0, column=0, padx=50, pady=5, sticky="nsew")

        self.solver_panel = MazeSolverPanel(self, self.canvas, solve_callback, self.app)
        self.solver_panel.grid(row=0, column=1, padx=50, pady=5, sticky="nsew")

    def _validate_inputs(self, maze_canvas: 'MazeCanvas',generate_callback, solve_callback) -> None:
        """
        Validate constructor inputs.
        """
        if not hasattr(maze_canvas, "update_maze"):
            raise TypeError("maze_canvas must be a MazeCanvas instance")
        if not callable(generate_callback) or not callable(solve_callback):
            raise TypeError("Callbacks must be callable")