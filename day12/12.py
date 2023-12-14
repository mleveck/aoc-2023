from collections import deque
from typing import NamedTuple
from itertools import groupby
from util import *
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

lines = input.splitlines()


class Record(NamedTuple):
    record: str
    chksum: tuple[int, ...]


records = []


def validate(record: str, chksum: tuple[int, ...]):
    broken_spring_counts = tuple(len(list(g)) for k, g in groupby(record) if k == "#")
    return chksum == broken_spring_counts


def records_from_template(tmpl: str):
    q = deque([tmpl])
    res = []
    while q:
        t = q.popleft()
        idx = t.find("?")
        if idx == -1:
            res.append(t)
        else:
            tmpl_working = t.replace("?", ".", 1)
            tmpl_broken = t.replace("?", "#", 1)
            q.append(tmpl_broken)
            q.append(tmpl_working)
    return res


for line in lines:
    rt, cst = line.split(" ")
    r = Record(rt, tuple(int(cs) for cs in cst.split(",")))
    records.append(r)

possible_cnts = []
for r, chksm in records:
    cnt = sum(1 for pr in records_from_template(r) if validate(pr, chksm))
    possible_cnts.append(cnt)

print(sum(possible_cnts))
