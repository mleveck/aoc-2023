from typing import List
from operator import sub
from itertools import starmap
from util import *
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

lines = input.splitlines()

histories = parse_matrix(f=int, s=input)


def proc_hist(hist: List[int]) -> int:
    hist_seq = [hist]
    while not all(e == 0 for e in hist):
        hist = list(starmap(sub, zip(hist[1:], hist[:-1])))
        hist_seq.append(hist)
    acc = 0
    for log_line in hist_seq[::-1]:
        acc = log_line[0] - acc
    return acc


print(sum(proc_hist(h) for h in histories))
