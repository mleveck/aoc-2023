from itertools import combinations
from util import *
import sys

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

for ri, rv in enumerate(grid):
    for ci, cv in enumerate(rv):
        if cv == "#":
            row_to_val.add(ri)
            col_to_val.add(ci)

new_grid = []
for ri, row in enumerate(grid):
    if ri not in row_to_val:
        new_grid.append(row)
        new_grid.append(row)
    else:
        new_grid.append(row)

final_grid = []
for row in new_grid:
    new_row = []
    for ci, col in enumerate(row):
        if ci not in col_to_val:
            new_row.append(col)
            new_row.append(col)
        else:
            new_row.append(col)
    final_grid.append(new_row)    

star_map = set()

for ri, row in enumerate(final_grid):
    for ci, col in enumerate(row):
        if col == "#":
            star_map.add((ri, ci))

dists =[]
for p1, p2 in combinations(star_map, 2):
    dists.append(abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))

print(sum(dists))

