from itertools import combinations
from util import *
import sys

N = 1_000_000

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

lines = input.splitlines()
grid = parse_matrix(s=input, col_sep="")


def print_grid(grid):
    for row in grid:
        print("".join(row))


row_to_val = set()
col_to_val = set()
star_map = set()
len(star_map)

for ri, rv in enumerate(grid):
    for ci, cv in enumerate(rv):
        if cv == "#":
            row_to_val.add(ri)
            col_to_val.add(ci)
            star_map.add((ri, ci))

star_list = sorted(list(star_map))
new_star_list = []

for star in star_list:
    empty_col_count = sum(1 for col in range(star[1]) if col not in col_to_val)
    empty_row_count = sum(1 for row in range(star[0]) if row not in row_to_val)
    new_star_list.append(
        (star[0] + (N - 1) * empty_row_count, star[1] + (N - 1) * empty_col_count)
    )

dists = []
for p1, p2 in combinations(new_star_list, 2):
    dists.append(abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))

print(sum(dists))
