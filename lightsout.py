"""Represent game state for Lights Out."""


class LightsOut:

    def __init__(self, size: int):
        if size <= 0:
            raise ValueError(f"size must be positive; not {size}")
        self._size = size
        # Bitmask representing a binary matrix in row-major format.
        self._state = 0

    def solved(self) -> bool:
        return self._state == 0
    
    def state(self) -> int:
        return self._state

    def _valid_pos(self, row: int, col: int) -> bool:
        return all(0 <= dim < self._size for dim in (row, col))

    def toggle(self, row: int, col: int):
        if not self._valid_pos(row, col):
            raise ValueError(
                f"Invalid position for grid size {self._size}: ({row}, {col}")
        mask = 2 ** (self._size * row + col)
        neighbors = [
            (row, col + 1), (row, col - 1), (row - 1, col), (row + 1, col)
        ]
        for n_row, n_col in neighbors:
            if not self._valid_pos(n_row, n_col):
                continue
            mask += 2 ** (self._size * n_row + n_col)
        self._state ^= mask
        