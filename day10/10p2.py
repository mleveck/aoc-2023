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


def type_of_s(sidx, first_idx, last_idx):
    dir_to_first = (first_idx[0] - sidx[0], first_idx[1] - sidx[1])
    dir_to_last = (last_idx[0] - sidx[0], last_idx[1] - sidx[1])
    for ptype, dirs in ptype_match_mat.items():
        if {dir_to_last, dir_to_first} == dirs:
            return ptype


adj_map = defaultdict(list)

start_idx = (None, None)


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
        winning_path = [start_idx] + path + [start_idx]
        max_travel = dest_dist + 1
    act_next_dests = [(d, dest_dist + 1) for d in possible_new_dests if d not in seen]
    if act_next_dests:
        next_dests.extend(act_next_dests)
    else:  # hit a dead end 0 out the path
        path = []


path = winning_path
stype_in_path = type_of_s(start_idx, path[1], path[-2])
path_set = set(winning_path)
candidate_list = [
    (r, c)
    for r in range(len(grid))
    for c in range(len(grid[0]))
    if (r, c) not in path_set
]


def move(point, direction):
    return (point[0] + direction[0], point[1] + direction[1])


def direction(pold, pnew):
    return (pnew[0] - pold[0], pnew[1] - pold[1])


path_idx_to_dir = dict()

for pi, pp in enumerate(path[1:]):
    current_dir = direction(path[pi], pp)
    path_idx_to_dir[pp] = current_dir


def east_intersections(point):
    num_intersections = 0
    while (
        point[0] > -1
        and point[0] < len(grid)
        and point[1] > -1
        and point[1] < len(grid[0])
    ):
        if point in path_set and (
            grid[point[0]][point[1]] in "|F7"
            or (grid[point[0]][point[1]] == "S" and stype_in_path in "|F7")
        ):
            num_intersections += 1
        point = move(point, (0, 1))
    return num_intersections


contained = {point for point in candidate_list if east_intersections(point) % 2 == 1}

print(len(contained))
