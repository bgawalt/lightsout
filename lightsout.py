"""Represent game state for Lights Out."""

import dataclasses


@dataclasses.dataclass(frozen=True)
class LightsOut:
    size: int
    state: int = 0

    def __post_init__(self):
        if self.size <= 0:
            raise ValueError(f"size must be positive; not {self.size}")
        if self.state < 0:
            raise ValueError(f"state must be non-negative; not {self.state}")
        if self.state >= (2 ** (self.size * self.size)):
            raise ValueError(f"state exceeds bounds for size {self.size}: ")

    def solved(self) -> bool:
        return self.state == 0

    def _valid_pos(self, row: int, col: int) -> bool:
        return all(0 <= dim < self.size for dim in (row, col))

    def toggle(self, row: int, col: int) -> 'LightsOut':
        if not self._valid_pos(row, col):
            raise ValueError(
                f"Invalid position for grid size {self.size}: ({row}, {col}")
        mask = 2 ** (self.size * row + col)
        neighbors = [
            (row, col + 1), (row, col - 1), (row - 1, col), (row + 1, col)
        ]
        for n_row, n_col in neighbors:
            if not self._valid_pos(n_row, n_col):
                continue
            mask += 2 ** (self.size * n_row + n_col)
        return dataclasses.replace(self, state=(self.state ^ mask))
        