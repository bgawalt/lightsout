"""Represent and explore game states for Lights Out.

Use main() to breadth-first-search for all states from which you can
eventually reach lights-out.  Just supply the board width (boards are square)
as the first argument. For a 4x4 grid:

  $  python3 lightsout.py 4

You're not going to believe this, but it has trouble even with exploring 5x5,
which is to say, a state space of 32 million values.
"""

import collections
import dataclasses
import sys


@dataclasses.dataclass(frozen=True)
class LightsOut:
    """State of a Lights Out game board.
    
    Attributes:
        size: The height/width of the square board.
        state: An integer, used as a bitmask, where each bit represents an
            element in the binary matrix of "which lights are on." Uses a
            row-major format; the first `size` bits are the first row of lights.
    """
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
        """Says if this is a solved board (i.e., all lights off: state 0)."""
        return self.state == 0

    def _valid_pos(self, row: int, col: int) -> bool:
        return all(0 <= dim < self.size for dim in (row, col))

    def toggle(self, row: int, col: int) -> 'LightsOut':
        """Returns the new state you get by pressing the light at (row, col).

        Args:
            row: The row of the light you pressed.
            col: The column of the light you pressed.
         
        Returns: toggles the given position, plus its NSEW neighbors.
        """
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


@dataclasses.dataclass(frozen=True)
class NextMove:
    row: int
    col: int
    to_go: int
    prev: int


def main():
    size = int(sys.argv[1])
    game = LightsOut(size)

    # Map [state] -> [move]
    parents = {game.state: NextMove(-1, -1, 0, -1)}
    depths = {game: 0}
    # The last state seen
    prev = -1
    # Initialize queue with the lights-out state:
    candidates = collections.deque([game,])
    next_trigger = 2
    while candidates:
        if len(parents) > next_trigger:
            next_trigger *= 2
            print(f"   ... found {len(parents)} states so far...")
        v = candidates.popleft()
        for r in range(size):
            for c in range(size):
                w = v.toggle(r, c)
                if w.state in parents:
                    continue
                depths[w] = depths[v] + 1
                parents[w.state] = NextMove(r, c, depths[v] + 1, v.state)
                candidates.append(w)
    print(f'{len(parents)} states reached, of {2 ** (size * size)} total.')
    max_depth = max(nm.to_go for nm in parents.values())
    print(f'Max depth: {max_depth}')


if __name__ == "__main__":
    main()