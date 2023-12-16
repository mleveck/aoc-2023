from typing import NamedTuple
from util import *
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

lines = input.splitlines()

contraption = parse_matrix(s=input, col_sep="")


class Mirror (NamedTuple):
    symbol: str
    flow_map: dict[tuple[int,int],tuple[tuple[int, int],...]]

class CellState(NamedTuple):
    symbol: str
    energized_from: set
    def copy(self):
        return CellState(self.symbol, self.energized_from.copy())

vsplit = Mirror("|", {(0, 1): ((-1, 0), (1, 0)),
                      (0, -1): ((-1, 0), (1, 0))
                    })

hsplit = Mirror("-", {(-1, 0): ((0,1), (0, -1)),
                      (1, 0): ((0,1), (0, -1))})

bslash = Mirror("\\", {(-1,0): ((0, 1),),
                       (1, 0): ((0, -1),),
                       (0, -1):((1, 0),),
                       (0, 1): ((-1, 0),)})
fslash = Mirror ("/", {(-1,0):((0, -1),),
                       (1, 0):((0, 1),),
                       (0, -1):((-1, 0),),
                       (0, 1):((1, 0),)})
dot = Mirror(".",{})

def point_add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def point_inv(p):
    return (-1*p[0], -1*p[1])

def point_sub(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

pieces = {"|": vsplit, "-": hsplit, "\\": bslash, "/": fslash, ".": dot}

start_grid = {(r,c):CellState(char, set()) for r, row in enumerate(lines) for c, char in enumerate(row)}
start_grid[(0, 0)].energized_from.add((0, -1))

def step(grid: dict[tuple[int,int], CellState]):
    new_grid = dict()
    for (r,c), cell in grid.items():
        if (r, c) not in new_grid:
            new_grid[(r,c)] = grid[(r,c)].copy()
        for source_dir in cell.energized_from:
            target_dirs = pieces[cell.symbol].flow_map.get(source_dir, None)
            if target_dirs:
                for target_dir in target_dirs:
                    target = point_add((r,c), target_dir)
                    if target in grid:
                        if target not in new_grid:
                            new_grid[target] = grid[target].copy()
                        new_grid[target].energized_from.add(point_sub((r, c), target))
            else:
                target_dir = point_inv(source_dir)
                target = point_add((r, c), target_dir)
                if target in grid:
                    if target not in new_grid:
                        new_grid[target] = grid[target].copy()
                    new_grid[target].energized_from.add(point_sub((r, c), target))
    return new_grid

def print_energy_state(grid):
    for r in range(len(contraption)):
        energy_state = ['#' if grid[(r,c)].energized_from else '.' for c in range(len(contraption[0]))]
        print("".join(energy_state))
    print("\n\n")

def simulate(grid):
    grid = grid
    new_grid = step(grid)
    while grid != new_grid:
        grid, new_grid = new_grid, simulate(new_grid)
    return new_grid

ans = sum(1 if c.energized_from else 0 for c in simulate(start_grid).values())
print(ans)
