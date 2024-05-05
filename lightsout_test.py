import lightsout

import random


def test_init_solved():
    game = lightsout.LightsOut(5)
    assert game.solved(), "initial games should be solved"


def test_init_state():
    game = lightsout.LightsOut(5)
    assert game.state == 0, f"\
        initial games should have state 0, not {game.state}"


def test_toggle_bad_pos():
    game = lightsout.LightsOut(5)
    bad_pos = [
        (-1, 3),
        (5, 3),
        (3, -1),
        (3, 5)
    ]
    for row, col in bad_pos:
        caught = False
        try:
            game.toggle(row, col)
        except ValueError:
            caught = True
        assert caught, f"\
            Failed to throw exception for ({row}, {col})"


def test_toggle_repeat():
    game = lightsout.LightsOut(5)
    for row in range(5):
        for col in range(5):
            game = game.toggle(row, col)
            assert game.state != 0, f"\
                Toggle at ({row}, {col}) produced a zero state"
            game = game.toggle(row, col)
            assert game.state == 0, f"\
                Repeat of ({row}, {col}) yielded non-zero state: {game.state}"


def test_state_size_one():
    game = lightsout.LightsOut(1)
    next = game.toggle(0, 0)
    assert next.state == 1, f"\
        Toggle at (0, 0) produced state {next.state}, not 1"


def test_state_size_two():
    game = lightsout.LightsOut(2)
    # Grid: 
    #   0 0
    #   0 0
    game = game.toggle(0, 0)
    # Grid: 
    #   1 1
    #   1 0
    assert game.state == 7, f"\
        Toggle at (0, 0) produced state {game.state}, not 7"
    game = game.toggle(1, 1)
    # Grid: 
    #   1 0
    #   0 1
    assert game.state == 9, f"\
        Toggle at (1, 1) produced state {game.state}, not 9"
    game = game.toggle(0, 1)
    # Grid: 
    #   0 1
    #   0 0
    assert game.state == 2, f"\
        Toggle at (1, 1) produced state {game.state}, not 2"
    game = game.toggle(1, 0)
    # Grid: 
    #   1 1
    #   1 1
    assert game.state == 15, f"\
        Toggle at (1, 1) produced state {game.state}, not 15"
    

def main():
    test_init_solved()
    test_init_state()
    test_toggle_bad_pos()
    test_toggle_repeat()
    test_state_size_one()
    test_state_size_two()
    print("All passed!!")


if __name__ == "__main__":
    main()