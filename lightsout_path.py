"""Print out the paths from all-on to lights-out, for 3-, 4-, and 5x5-grids.

Prerequisite: run `lightsout.py` to generate a SQLite DB file full of
"from this state, click here to move towards lights-out" records.

Usage:

  $ python lightsout_path.py lightsout_state.db
"""

import dataclasses
import sqlite3
import sys


@dataclasses.dataclass
class NextStep:
    row: int
    col: int
    dest: int


def load_state_lookup(
        cur: sqlite3.Cursor,
        grid_size: int
) -> dict[int, NextStep]:
    """Loads the single-steps of all paths to lights-out."""
    out = {}
    cur.execute(f"""
        SELECT
            state,
            row,
            col,
            destination_state
        FROM lightsout_states
        WHERE size = {grid_size}
    """)
    batch = cur.fetchmany(100)
    while batch:
        for state, row, col, dest in batch:
            if state in out:
                raise RuntimeError(f'Duplicate entry: {state}')
            out[state] = NextStep(row=row, col=col, dest=dest)
        batch = cur.fetchmany(100)
    return out


def main():
    conn = sqlite3.connect(sys.argv[1])
    grid_size = int(sys.argv[2])
    for grid_size in (3, 4, 5):
        lookup = load_state_lookup(conn.cursor(), grid_size)
        print(f'{grid_size} x {grid_size} solution:')
        curr = (2 ** (grid_size * grid_size)) - 1
        while curr != 0:
            next = lookup[curr]
            print('\t%x: (%d, %d)' % (curr, next.row, next.col))
            curr = next.dest
        print('')


if __name__ == "__main__":
    main()