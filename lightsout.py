"""Represent game state for Lights Out.

TODO: It's great that this works, but now I need to swap away from a literal
representation of [][]bool and to a purely integer representation. And each
LightsOut object should be immutable, and toggle should return a new one instead
of mutating local state.
"""


class LightsOut:

    def __init__(self, size: int):
        if size <= 0:
            raise ValueError(f"size must be positive; not {size}")
        self._size = size
        self._grid = [
            [False for _ in range(size)]
            for _ in range(size)
        ]

    def solved(self) -> bool:
        for row in self._grid:
            if any(row):
                return False
        return True
    
    def state(self) -> int:
        state = 0
        k = 0
        for row in self._grid:
            for elem in row:
                if elem:
                    state += (2 ** k)
                k += 1
        return state

    def _valid_pos(self, row: int, col: int) -> bool:
        for direction in (row, col):
            if direction < 0 or direction >= self._size:
                return False
        return True

    def toggle(self, row: int, col: int):
        if not self._valid_pos(row, col):
            raise ValueError(
                f"Invalid position for grid size {self._size}: ({row}, {col}")
        self._grid[row][col] = not self._grid[row][col]
        neighbors = [
            (row, col + 1), (row, col - 1), (row - 1, col), (row + 1, col)
        ]
        for n_row, n_col in neighbors:
            if not self._valid_pos(n_row, n_col):
                continue
            self._grid[n_row][n_col] = not self._grid[n_row][n_col]
        