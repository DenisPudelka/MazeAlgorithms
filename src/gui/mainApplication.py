from .mazeCanvas import MazeCanvas
from .newSouthPanel import *
from src.algorithms.generate_maze.randomizedPrimsAlgorithm import *
from src.algorithms.generate_maze.randomizesDepthFirstSearchAlgorithm import *
from src.algorithms.generate_maze.randomizedKruskalsAlgorithm import *
from src.maze.maze import *
from src.algorithms.generate_maze.wilsonAlgorithm import WilsonAlgorithm
from src.algorithms.generate_maze.fractalTessellationAlgorithm import FractalTessellationAlgorithm
from src.algorithms.generate_maze.recusiveDivisionAlgorithm import RecursiveDivisionAlgorithm
from src.algorithms.solve_maze.depthFirstSearchSolver import DepthFirstSearchSolver
from src.algorithms.solve_maze.breadthFirstSearchSolver import BreadthFirstSearchSolver
from src.algorithms.solve_maze.aStarSearchSolver import AStarSearchSolver
from src.algorithms.solve_maze.dijkstraSolver import DijkstraSolver
from src.algorithms.solve_maze.greedyBestFirstSearchSolver import GreedyBestFirstSearchSolver


class MainApplication(tk.Tk):
    """
    Main application window for the Maze Generator/Solver.
    This class serves as the root container for all UI components and coordinates between the visualization and controls.
    """
    ANIMATION_DELAY_MS = 5

    def __init__(self):
        super().__init__()
        self.title("Maze Application")
        self.geometry("650x700")
        self.pick_mode = None

        # GUI components
        self.maze_canvas = MazeCanvas(self)
        self.maze_canvas.pack(side="top", fill="both", expand=True)
        self.south_panel = SouthControlPanel(self, self.maze_canvas, self.generate_maze, self.solve_maze, self)
        self.south_panel.pack(side="bottom", fill="both")

    def generate_maze(self, width: int, height: int, algorithm: str, isAnimation: bool) -> None:
        """
        Generate a new maze using the specified algorithm.
        The available algorithms are mapped to their respective strategy classes.
        """
        if not self.check_input(width, height, algorithm):
            return

        strategies = {
            'Randomized Prims': RandomizedPrimesAlgorithm,  # **
            'Depth First Search': DepthFirstSearch,
            'Kruskals Algorithm': RandomizedKruskalAlgorith,  # **
            'Wilson Algorithm': WilsonAlgorithm,
            'Fractal Tessellation Algorithm': FractalTessellationAlgorithm,
            'Recursive Division': RecursiveDivisionAlgorithm
        }
        generation_strategy = strategies[algorithm]()

        self.maze = Maze(width, height, generation_strategy, isAnimation)

        # Animate maze generation
        if self.maze.isAnimation:
            def on_step(matrix):
                self.maze_canvas.update_maze(matrix)
                self.update_idletasks()
                self.after(self.ANIMATION_DELAY_MS)

            self.maze.set_callback(on_step)

        self.maze.generate_maze()

        self.maze_canvas.update_maze(self.maze.maze_matrix)

        if self.maze is not None:
            self.maze.start = None
            self.maze.end = None
            self.south_panel.solver_panel.update_start_label("Not picked")
            self.south_panel.solver_panel.update_end_label("Not picked")


    def check_input(self, width: int, height: int, algorithm: str) -> bool:
        """
        Validating user inputs for maze generation.
        """
        try:
            if not isinstance(width, int) or not isinstance(height, int):
                raise ValueError("Width and Height must be integers")

            if width < 10 or height < 10:
                raise ValueError("Minimum allowed size is 10x10")

            if width > 65 or height > 65:
                raise ValueError("Maximum allowed size is 64x64")

            requires_odd = {"Depth First Search", "Kruskals Algorithm", "Wilson Algorithm"}
            if algorithm in requires_odd:
                if width % 2 == 0 or height % 2 == 0:
                    raise ValueError(f"{algorithm} requires odd dimensions (e.g., 11x11)")

            return True
        except ValueError as e:
            self.errorMessage("Warning", str(e))
            return False


    def errorMessage(self, title: str, message: str) -> None:
        """
        Display error message.
        """
        messagebox.showwarning(title=title, message=message)


    def on_tile_clicked(self, position: Tuple[int, int]) -> None:
        """
        Handles tile clicks for start/end selection.
        """
        if not self.maze:
            return

        x, y = position
        if self.maze.maze_matrix[y][x] == Maze.WALL:
            return

        if self.pick_mode == "start":
            # Clearing old start position
            if self.maze.start is not None:
                old_position = self.maze.start
                self.maze.modify_maze(old_position, '1')

            # New start position
            self.maze.start = position
            self.maze.modify_maze(position, 'S')
            self.south_panel.solver_panel.update_start_label(position)
        elif self.pick_mode == "end":
            # Clearing old end position
            if self.maze.end is not None:
                old_position = self.maze.end
                self.maze.modify_maze(old_position, '1')

            # New end position
            self.maze.end = position
            self.maze.modify_maze(position, 'E')
            self.south_panel.solver_panel.update_end_label(position)

        self.maze_canvas.update_maze(self.maze.maze_matrix)
        self.pick_mode = None

    def update_position(self, position: Tuple[int, int], marker: str, label_type: str) -> None:
        pass

    def solve_maze(self, algorithm: str, isAnimation: bool) -> None:
        """
        Solve maze using the specified algorithm.
        """
        if not self.maze or not self.maze.start or not self.maze.end:
            self.errorMessage("Error", "Please generate maze and pick Start and End points")
            return

        # Removing old path markers ('P') from the maze - P: path finding
        for y in range(self.maze.maze_matrix.shape[0]):
            for x in range(self.maze.maze_matrix.shape[1]):
                if self.maze.maze_matrix[y][x] == 'P':
                    self.maze.maze_matrix[y][x] = '1'

        strategies = {
            'DepthFirstSearch': DepthFirstSearchSolver,
            'BreadthFirstSearch': BreadthFirstSearchSolver,
            'A*': AStarSearchSolver,
            'Dijkstra': DijkstraSolver,
            'GreedyBestFirstSearch': GreedyBestFirstSearchSolver
        }

        solver_class = strategies.get(algorithm)

        if not solver_class:
            self.errorMessage("Error", f"Solver for {algorithm} not found.")
            return

        solver = solver_class()

        if isAnimation:
            def on_step(matrix):
                self.maze_canvas.update_maze(matrix)
                self.update_idletasks()
                self.after(20)

            solver.solve_maze(self.maze, on_step)
        else:
            solver.solve_maze(self.maze)

        self.maze_canvas.update_maze(self.maze.maze_matrix)
        self.pick_mode = None
