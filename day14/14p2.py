from typing import Counter 
from itertools import islice
from enum import Enum
from util import *
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

lines = input.splitlines()

N = 1_000_000_000
grid = parse_matrix(s=input, col_sep="")
cols = [list(c) for c in zip(*grid)]


def print_grid(g):
    for r in g:
        print("".join(r))
    print("\n")


class Dir(Enum):
    North = 1
    West = 2
    South = 3
    East = 4


def tilt(grid, d):
    match d:
        case Dir.North:
            coll = list(list(c) for c in zip(*grid))
            shift(coll)
            return tuple(tuple(c) for c in zip(*coll))
        case Dir.South:
            coll = list(list(reversed(c)) for c in zip(*grid))
            shift(coll)
            return tuple(zip(*tuple(c[::-1] for c in coll)))
        case Dir.West:
            coll = list(list(r) for r in grid)
            shift(coll)
            return tuple(tuple(c) for c in coll)
        case Dir.East:
            coll = list(list(reversed(r)) for r in grid)
            shift(coll)
            return tuple(tuple(reversed(r)) for r in coll)


def shift(collection):
    for col in collection:
        for j, val in enumerate(col):
            if val == "O":
                i = j
                while i > 0:
                    if col[i] == "O" and col[i - 1] == ".":
                        col[i], col[i - 1] = ".", "O"
                    else:
                        break
                    i -= 1


def score(grid):
    ans = 0
    for i, r in enumerate(grid):
        c = Counter(r)
        n_rocks = c.get("O", 0)
        score = n_rocks * (len(grid) - i)
        ans += score
    return ans


def spin_cyle(grid):
    new_grid = grid
    for dir in Dir:
        new_grid = tilt(new_grid, dir)
    return new_grid


def repeat_cycle(grid):
    iter_grid = grid
    while True:
        iter_grid = spin_cyle(iter_grid)
        yield iter_grid


grid_key = tuple(tuple(r) for r in grid)
seen = {grid_key: 0}
grid_r = grid_key
cycle_len = None
cycle_start = None
cycle_grid = None

for i in range(1, N):
    grid_r = spin_cyle(grid_r)
    if grid_r in seen:
        cycle_grid = grid_r
        cycle_start = seen[grid_r]
        cycle_len = i - cycle_start
        break
    seen[grid_r] = i

num_effective_spins = (N - cycle_start) % cycle_len

last_spin_cycles = list(islice(repeat_cycle(cycle_grid), num_effective_spins))
print(score(last_spin_cycles[-1]))
