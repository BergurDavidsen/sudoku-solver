import time

class SudokuSolver:
    def __init__(self, board):
        self.board = board

    def get_box(self, row, col):
        box = []
        box_start_row = (row // 3) * 3
        box_start_col = (col // 3) * 3
        for r in range(box_start_row, box_start_row + 3):
            for c in range(box_start_col, box_start_col + 3):
                box.append(self.board[r][c])
        return box

    def get_possible_values(self, row, col):
        if self.board[row][col] != 0:
            return []

        used = set(self.board[row])
        used |= {self.board[r][col] for r in range(9)}
        used |= set(self.get_box(row, col))
        return [n for n in range(1, 10) if n not in used]

    def find_most_constrained_cell(self):
        """Find the empty cell with the fewest legal values (MRV heuristic)."""
        min_options = 10  # More than max possible
        best_cell = None
        best_options = []

        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    options = self.get_possible_values(row, col)
                    if len(options) < min_options:
                        min_options = len(options)
                        best_cell = (row, col)
                        best_options = options
                        if min_options == 1:
                            return best_cell, best_options  # Optimal

        return best_cell, best_options

    def solve(self):
        start_time = time.time()
        solved = self._solve_recursive()
        end_time = time.time()
        print(f"solve time: {round((end_time - start_time) * 1000, 5)}ms")
        return solved

    def _solve_recursive(self):
        cell, options = self.find_most_constrained_cell()
        if cell is None:
            return True  # Board is filled

        row, col = cell
        if not options:
            return False  # Forward check fail

        for val in options:
            self.board[row][col] = val
            if self._solve_recursive():
                return True
            self.board[row][col] = 0  # Backtrack

        return False
