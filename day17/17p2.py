from collections import defaultdict
from typing import NamedTuple
from operator import itemgetter
from dataclasses import dataclass
from heapq import heappush, heappop
from util import *
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

lines = input.splitlines()

grid = parse_matrix(s=input, f=int, col_sep="")
points2cost = {(r, c): val for r, row in enumerate(grid) for c, val in enumerate(row)}


class Dest(NamedTuple):
    coord: tuple[int, int]
    dir: tuple[int, int]
    count: int


@dataclass(order=True)
class NodeState:
    path_cost: float = float("inf")
    parent: Dest | None = None
    finished: bool = False


def next_dests(current_coord, current_dir, count):
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    backwards = point_inv(current_dir)
    if backwards in dirs:
        dirs.remove(backwards)
    if count >= 10:
        if current_dir in dirs:
            dirs.remove(current_dir)
    if count < 4:
        dirs = [current_dir]
    return [
        Dest(dest_coord, dir, count + 1 if dir == current_dir else 1)
        for dir in dirs
        if (dest_coord := point_add(current_coord, dir)) in points2cost
    ]


def djikstra(starts: list[Dest]):
    node_states: dict[Dest, NodeState] = defaultdict(NodeState)
    q = [(0.0, start) for start in starts]
    for start in starts:
        node_states[start] = NodeState(path_cost=0.0)
    while q:
        curr_cost, node = heappop(q)
        if node_states[node].finished:
            continue
        node_states[node].finished = True
        dests = next_dests(*node)
        for dest in dests:
            if node_states[dest].finished:
                continue
            new_path_cost = curr_cost + points2cost[dest.coord]
            if new_path_cost < node_states[dest].path_cost:
                node_states[dest] = NodeState(parent=node, path_cost=new_path_cost)
                heappush(q, (new_path_cost, dest))
    return node_states


path_map = djikstra(
    [Dest(coord=(0, 0), dir=(0, 1), count=0), Dest(coord=(0, 0), dir=(1, 0), count=0)]
)

min_dest = min(
    [
        (k, v)
        for k, v in path_map.items()
        if k.coord == (len(grid) - 1, len(grid[0]) - 1) and k.count >= 4
    ],
    key=itemgetter(1),
)
#### debug
min_path = [min_dest[0]]
curr_node = min_dest[0]
while parent := path_map[curr_node].parent:
    min_path.append(parent)
    curr_node = parent


def dir2str(dir):
    m = {(0, 1): ">", (1, 0): "v", (-1, 0): "^", (0, -1): "<"}
    return m[dir]


def path2str(path_map, grid):
    s = ""
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if (r, c) in path_map:
                s += dir2str(path_map[(r, c)].dir)
            else:
                s += str(val)
        s += "\n"
    return s


min_path = list(reversed(min_path))
coord2pathdest = {dest.coord: dest for dest in min_path}
# print(path2str(coord2pathdest, grid))
# debug

print(min_dest[1].path_cost)
