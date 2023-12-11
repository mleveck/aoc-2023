from collections import defaultdict
from util import *
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

lines = input.splitlines()
grid = parse_matrix(s=input, col_sep="")

ptype_match_mat = {
    "F": {(0, 1), (1, 0)},
    "7": {(0, -1), (1, 0)},
    "|": {(1, 0), (-1, 0)},
    "-": {(0, -1), (0, 1)},
    "L": {(-1, 0), (0, 1)},
    "J": {(0, -1), (-1, 0)},
}


def valid_neighbor(el_ri, el_ci, n_ri, n_ci):
    el_val = grid[el_ri][el_ci]
    n_val = grid[n_ri][n_ci]
    if n_val == "." or el_val == ".":
        return False
    if el_val == "S":
        return valid_neighbor(n_ri, n_ci, el_ri, el_ci)
    for valid_dir in ptype_match_mat[el_val]:
        if el_ri + valid_dir[0] == n_ri and el_ci + valid_dir[1] == n_ci:
            return True
    return False


# Create Adjacency map and figure out where our start is
adj_map = defaultdict(list)
start_idx = (None, None)
for ri, row in enumerate(grid):
    for ci, col in enumerate(row):
        if col == "S":
            start_idx = (ri, ci)
        if col == "S" or col in ptype_match_mat.keys():
            neighbor_idxs = potential_neighbors(ri, ci, grid)
            act_neighbors = [
                n for n in neighbor_idxs if valid_neighbor(ri, ci, n[0], n[1])
            ]
            adj_map[(ri, ci)].extend(act_neighbors)

# find the longest path going through adjacency map graph
seen = {start_idx}
max_travel = -1
next_dests = [(idx, 1) for idx in adj_map[start_idx]]
path = []
winning_path = []
while next_dests:
    dest, dest_dist = next_dests.pop()
    path.append(dest)
    seen.add(dest)
    possible_new_dests = adj_map[dest]
    if (
        any(grid[d[0]][d[1]] == "S" for d in possible_new_dests)
        and dest_dist + 1 > max_travel
    ):
        winning_path = path + [start_idx]
        max_travel = dest_dist + 1
    act_next_dests = [(d, dest_dist + 1) for d in possible_new_dests if d not in seen]
    if act_next_dests:
        next_dests.extend(act_next_dests)
    else:  # hit a dead end 0 out the path
        path = []

print(len(set(winning_path)) // 2)  # parity check
print(max_travel // 2)  # ans
