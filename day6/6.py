from typing import List
from operator import *
from util import *
from collections import *
from functools import *
from itertools import *
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

lines = input.splitlines()

table = [l.split(":")[1].strip().split() for l in lines]
tablen = [[int(c) for c in r] for r in table] 

races = list(zip(tablen[0], tablen[1]))


ways2win =[]
for time, dist in races:
    winning_combos = []
    for t in range(time):
        dtrav = (time - t)*t
        if dtrav > dist:
            winning_combos.append(t)
    ways2win.append(len(winning_combos))
print(reduce(mul, ways2win))





