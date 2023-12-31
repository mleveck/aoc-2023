from itertools import cycle
from util import *
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

lines = input.splitlines()

instructions, mtxt = lines[0], lines[2:]

keys = list(l.split(" = ")[0] for l in mtxt)
lrvals = list(tuple(l.split(" = ")[1].strip("(").strip(")").split(", ")) for l in mtxt)

map = dict(zip(keys, lrvals))

val = 'AAA'
steps = 0
for dir in cycle(instructions):
    if dir == "R":
        val = map[val][1]
    if dir == "L":
        val = map[val][0]
    steps +=1
    if val[-1] == 'Z':
        break

print(steps)
    



