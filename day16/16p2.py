from typing import List, NamedTuple
from util import *
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

lines = input.splitlines()


class Mirror(NamedTuple):
    symbol: str
    flow_map: dict[tuple[int, int], tuple[tuple[int, int], ...]]


class CellUpdate(NamedTuple):
    char: str
    coord: tuple[int, int]
    energized_from: tuple[int, int]


def point_add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])


def point_inv(p):
    return (-1 * p[0], -1 * p[1])


def point_sub(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])


grid = parse_matrix(s=input, col_sep="")
COL_LEN = len(grid[0])
ROW_LEN = len(grid)

vsplit = Mirror("|", {(0, 1): ((-1, 0), (1, 0)), (0, -1): ((-1, 0), (1, 0))})

hsplit = Mirror("-", {(-1, 0): ((0, 1), (0, -1)), (1, 0): ((0, 1), (0, -1))})

bslash = Mirror(
    "\\",
    {(-1, 0): ((0, 1),), (1, 0): ((0, -1),), (0, -1): ((1, 0),), (0, 1): ((-1, 0),)},
)
fslash = Mirror(
    "/",
    {(-1, 0): ((0, -1),), (1, 0): ((0, 1),), (0, -1): ((-1, 0),), (0, 1): ((1, 0),)},
)
dot = Mirror(".", {})

pieces = {"|": vsplit, "-": hsplit, "\\": bslash, "/": fslash, ".": dot}

grid_coords = {
    (r, c): char for r, row in enumerate(lines) for c, char in enumerate(row)
}


def energize_cells(cell_update_stack: List[CellUpdate]):
    seen = set()
    energized = set()
    while cell_update_stack:
        update = cell_update_stack.pop()
        energized.add(update.coord)
        seen.add(update)
        potential_target_coords = [
            point_add(update.coord, dir)
            for dir in pieces[update.char].flow_map.get(update.energized_from, [])
        ]
        if not potential_target_coords:
            potential_target_coords = [
                point_add(update.coord, point_inv(update.energized_from))
            ]
        new_updates = [
            new_update
            for coord in potential_target_coords
            if coord in grid_coords
            if (
                new_update := CellUpdate(
                    coord=coord,
                    char=grid_coords[coord],
                    energized_from=point_sub(update.coord, coord),
                )
            )
            not in seen
        ]
        cell_update_stack.extend(new_updates)
    return energized


top_starts = [
    [CellUpdate(coord=(0, c), char=grid_coords[(0, c)], energized_from=(-1, 0))]
    for c in range(COL_LEN)
]
bottom_starts = [
    [
        CellUpdate(
            coord=(len(grid) - 1, c),
            char=grid_coords[(ROW_LEN - 1, c)],
            energized_from=(1, 0),
        )
    ]
    for c in range(COL_LEN)
]
right_starts = [
    [CellUpdate(coord=(r, 0), char=grid_coords[(r, 0)], energized_from=(0, -1))]
    for r in range(ROW_LEN)
]
left_starts = [
    [
        CellUpdate(
            coord=(r, len(grid[0]) - 1),
            char=grid_coords[(r, COL_LEN - 1)],
            energized_from=(0, 1),
        )
    ]
    for r in range(ROW_LEN)
]

energized_counts = [
    len(energize_cells(start))
    for start in top_starts + bottom_starts + right_starts + left_starts
]
print(max(energized_counts))
