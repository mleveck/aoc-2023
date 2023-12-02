from collections.abc import Callable
from functools import partial
from typing import Any


def identity(v: Any) -> Any:
    return v


def slurp(fname):
    with open(fname) as f:
        s = f.read().strip()
        return s


def psplitlines(f: Callable = identity, s: str = ""):
    l = s.splitlines()
    return list(map(f, l))


def psplitdlines(f: Callable = identity, s: str = ""):
    l = s.split("\n\n")
    return list(map(f, l))


def parse_matrix(f=identity, s: str = "", col_sep=" ", row_sep="\n"):
    rows = s.split(row_sep)
    matrix = map(lambda s: s.split(col_sep), rows)
    processed_matrix = [[f(el) for el in col] for col in matrix]
    return processed_matrix

dydx= [(dy,dx) for dx in [0, 1, -1] for dy in [1, 0, -1] if not dy == dx == 0]

def potential_neighbors(row, col, grid=None):
    pn = [(row + dy, col + dx) for dy, dx in dydx]
    if grid:
        pn = [coord for coord in pn if 0 <= coord[0] < len(grid) and 0 <= coord[1] < len(grid[0])]
    return pn

digit_words = "zero one two three four five six seven eight nine".split()

if __name__ == "__main__":
    sample = """1 2 3
4 5 6
7 8 9"""

    sample2 = """34
45
64

56
78
89"""

    
    potential_neighbors(2, 2, parse_matrix(int, s=sample)) # [(4, 4), (2, 4), (4, 5), (3, 5), (2, 5), (4, 3), (3, 3), (2, 3)]
# [(1, 2), (2, 1), (1, 1)]
    parse_matrix(int, s=sample)

    psplitdlines(partial(psplitlines, int), sample2)
    psplitdlines(s=sample2)

    parse_matrix(int, s=sample)
