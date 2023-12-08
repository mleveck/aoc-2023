from math import lcm
from itertools import cycle
from util import *
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./input.txt").read().strip()

lines = input.splitlines()

instructions, mtxt = lines[0], lines[2:]

keys = list(l.split(" = ")[0] for l in mtxt)
lrvals = list(tuple(l.split(" = ")[1].strip("(").strip(")").split(", ")) for l in mtxt)

map = dict(zip(keys, lrvals))

starts = tuple(k for k in keys if k[-1] == 'A')

stepcounts = []

for val in starts:
    steps = 0
    for dir in cycle(instructions):
        if dir == "R":
            val = map[val][1]
        if dir == "L":
            val = map[val][0]
        steps +=1
        if val[-1] == 'Z':
            break
    stepcounts.append(steps)
print(lcm(*stepcounts))
