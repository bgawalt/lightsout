# Lights Out

Here's a simple puzzle game my kids like to play on my phone. You try and get
all the lights to go out.

Play the [4x4 grid here](https://gawalt.com/lightsout/4x4.html) and the *much
harder* [5x5 grid here](https://gawalt.com/lightsout/5x5.html).

Here's me teaching myself the basics of the HTML, CSS, JavaScript
trinity, using jQuery as the DOM modifier.

I started this a looong time ago, in Feb 2015, but never really got
into appropriate shape for public consumption. But now it is!

## The game: `4x4.html`, `5x5.html`, `style.css`, & `lightsout.js`

### Rules

The game board is a grid of lights. Initially, all the lights are on. Your goal
is to turn all the lights out (as fast as you can). Clicking a light toggles
that light you clicked, but also toggles the lights that are immediately north,
south, east, or west of it. Puzzling!

### Implementation

The game itself is playable by just loading `4x4.html` or `5x5.html` in your
browser. Its dependencies are all here, locally: `style.css`, `lightsout.js`,
and a copy of jQuery 1.11.2.

### TODO

*  Explain the rules and just generally spruce up `index.html`
*  Allow for starting from random initial states (from which it's possible to
   win!)
*  Build a HINT button that tells you what light will take you closer to
   lights-out
*  Figure out why WebKit hates this and won't render a square grid


## The solver: `lightsout.py`

### Python solver: `lightsout.py`

Per some of the above TODOs, I got curious about game states. If you play
optimally, how many turns does it take to get an all-on initial state, to the
all-off win state? For a (square) board of size `k`, how many of the `2^(k*k)`
possible states are ones from which you can reach lights-out?

So I wrote a solver in Python. It does breadth first search of game states:

1.  A grid of size `k` can be in one of `2^(k*k)` possible states. Call each 
    state a vertex in a graph.
2.  If your grid in is in state `S`, there are `k*k` states you could switch to
    (by toggling any one of the `k*k` lights in the grid).  Call those switches
    the edges of a graph.
3.  If you start at the state where all lights are off, you can use an
    exhaustive breadth first search of the graph to find all states from which
    you can win the game: "what states are connected to the win state?"
4.  And because it's breadth-first, each time you discover a new state, you can
    track the state from which you discovered it: if the grid is in state `S`,
    and toggling the light at `(row a, col b)` discovers a new state `T`, you
    now know that a path from `T` to the win state exists and flows through `S`.
    (And to get to `S` from `T`, just toggle the light at `(a, b)`).

`2^(k*k)` gets very big, very quick -- 33 million, for the standard 5x5 grid.
But the solver was able to find all reachable-from-lights-out states in about
20 minutes.

There's a test suite in `lightsout_test.py`, but I am too lazy to set up an
actual testing framework. 

### Results table: `lightsout_states`

The solver inserts its results to a SQLite3 table (for a SQLite file whose path
you specify) called `lightsout_states`. That tables columns are all integers,
and are named:

*  `size`: The size of the grid
*  `state`: A bitset representation of a grid state. It serializes the grid
    positions in row-major fashion: the least-significant `size` bits are the
    first row of lights; the next least `size` bits are the second row, etc.
    A bit value of 0 means the light is off.
*   `row`, `col`: Values in the range `[0, size)` that indicate which light you
    should toggle to get one step closer to lights-out from `state`.
*   `to_go`: How many steps will it take to get from `state` to lights-out?
*   `destination_state`: The state you'll reach when you toggle `row, col`.

I have not actually included a results DB file here, cuz it's just kinda large.

Fun facts:

*   For the three grids I've solved (3x3, 4x4, 5x5), all of them include "all
    lights on" as a state from which you can reach lights-out.
*   The longest optimally-played 5x5 games take 15 moves to win. There's 7,350
    such states that require you to make 15 moves, and "all lights on" is one of
    them.
*   The longest optimally-played 3x3 game takes 9 moves to win, and it's *not*
    the "all lights on" state. It's state 341! On a 3x3 grid, "all lights on"
    is only five hops away from winning. State 341 is `0b1010101101`, which is
    to say it looks like a checkerboard where the corner and center lights are
    on and the "side" lights are off.

### Solution from "all lights on": `lightsout_path`

You can print out a step-by-step path from all-on to lights-out with
`lightsout_path.py`:

```shell
$ python3 lightsout_path.py lightsout_states.db 4
3 x 3 solution:
        1ff: (2, 2)
        5f: (2, 0)
        97: (1, 1)
        2d: (0, 2)
        b: (0, 0)

4 x 4 solution:
        ffff: (3, 2)
        1bff: (2, 0)
        8ef: (1, 3)
        27: (0, 1)

5 x 5 solution:
        1ffffff: (4, 4)
        77ffff: (4, 2)
        95ffff: (4, 1)
        e4ffff: (3, 3)
        6adfff: (3, 2)
        2dcfff: (3, 1)
        e47ff: (2, 4)
        625ff: (2, 3)
        254ff: (2, 2)
        6c7f: (1, 4)
        2f6f: (1, 3)
        ce7: (1, 1)
        405: (1, 0)
        64: (0, 1)
        23: (0, 0)
```

Light-toggles commute, so you can do the steps in those paths in any order.

### TODO

*  The SQLite file winds up being surprisingly large: 202 MB. And `gzip --best`
   only gets that down to 85 MB. I should probably drop the duplicative info
   like `destination_state` and `to_go`.