from collections import deque
import time

class SudokuSolverCSP:
    def __init__(self, board):
        self.board = board
        self.domains = self.initialize_domains()

    def initialize_domains(self):
        domains = {}
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != 0:
                    domains[(row, col)] = [self.board[row][col]]
                else:
                    domains[(row, col)] = self.get_possible_values(row, col)
        return domains

    def get_neighbors(self, row, col):
        neighbors = set()
        for i in range(9):
            if i != col:
                neighbors.add((row, i))
            if i != row:
                neighbors.add((i, col))
        
        box_start_row = (row // 3) * 3
        box_start_col = (col // 3) * 3
        for r in range(box_start_row, box_start_row + 3):
            for c in range(box_start_col, box_start_col + 3):
                if (r, c) != (row, col):
                    neighbors.add((r, c))
        return neighbors

    def ac3(self):
        queue = deque()
        for cell in self.domains:
            for neighbor in self.get_neighbors(*cell):
                queue.append((cell, neighbor))

        while queue:
            xi, xj = queue.popleft()
            if self.revise(xi, xj):
                if not self.domains[xi]:
                    return False
                for xk in self.get_neighbors(*xi):
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, xi, xj):
        revised = False
        for x in self.domains[xi][:]:
            if all(x == y for y in self.domains[xj]):
                self.domains[xi].remove(x)
                revised = True
        return revised

    def get_possible_values(self, row, col):
        used = set(self.board[row])
        used |= {self.board[r][col] for r in range(9)}
        box = []
        box_start_row = (row // 3) * 3
        box_start_col = (col // 3) * 3
        for r in range(box_start_row, box_start_row + 3):
            for c in range(box_start_col, box_start_col + 3):
                box.append(self.board[r][c])
        used |= set(box)
        return [n for n in range(1, 10) if n not in used]

    def select_unassigned_variable(self):
        unassigned = [(cell, self.domains[cell]) for cell in self.domains if self.board[cell[0]][cell[1]] == 0]
        if not unassigned:
            return None, None
        # MRV
        unassigned.sort(key=lambda item: len(item[1]))
        return unassigned[0]

    def order_domain_values(self, cell):
        # LCV: sort by how few neighbors it restricts
        row, col = cell
        value_counts = {}
        for val in self.domains[cell]:
            count = 0
            for neighbor in self.get_neighbors(row, col):
                if val in self.domains.get(neighbor, []):
                    count += 1
            value_counts[val] = count
        return sorted(self.domains[cell], key=lambda v: value_counts[v])

    def is_assignment_valid(self, row, col, val):
        # Quick validity check
        for i in range(9):
            if self.board[row][i] == val or self.board[i][col] == val:
                return False
        box_start_row = (row // 3) * 3
        box_start_col = (col // 3) * 3
        for r in range(box_start_row, box_start_row + 3):
            for c in range(box_start_col, box_start_col + 3):
                if self.board[r][c] == val:
                    return False
        return True

    def solve(self):
        start = time.time()
        if not self.ac3():
            print("AC-3 detected inconsistency.")
            return False
        solved = self._backtrack()
        end = time.time()
        print(f"Solve time: {round((end - start) * 1000, 5)}ms")
        return solved

    def _backtrack(self):
        cell, domain = self.select_unassigned_variable()
        if cell is None:
            return True

        row, col = cell
        for val in self.order_domain_values(cell):
            if self.is_assignment_valid(row, col, val):
                self.board[row][col] = val
                backup_domains = self.domains.copy()
                self.domains[cell] = [val]
                if self._backtrack():
                    return True
                self.domains = backup_domains
                self.board[row][col] = 0

        return False
