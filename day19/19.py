from typing import NamedTuple
from collections import defaultdict
from operator import gt, lt
from functools import partial
from util import *
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

wftxt, partstxt = input.split("\n\n")

OPMAP = {">": gt, "<": lt}


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int


A = []
R = []
parts = []
workflows = defaultdict(list)


def place(bin, part):
    if bin == "A":
        A.append(part)
        return False
    if bin == "R":
        R.append(part)
        return False
    assert False


def apply_rule(part_key, thresh, op, action):
    def rule(part):
        if op(getattr(part, part_key), int(thresh)):
            return action
        return None

    return rule


def constantly(v):
    return lambda _: v


workflows["A"] = [partial(place, "A")]
workflows["R"] = [partial(place, "R")]

for line in partstxt.splitlines():
    line = line.strip("{").strip("}")
    attrs = line.split(",")
    parts.append(Part(*[int(attr.split("=")[1]) for attr in attrs]))

for line in wftxt.splitlines():
    name, rest = line.split("{")
    rest = rest.strip("}")
    rules = rest.split(",")
    for rule in rules:
        rparts = rule.split(":")
        if len(rparts) == 2:
            condition, action = rparts[0], rparts[1]
            for opkey in OPMAP.keys():
                if opkey in condition:
                    op = OPMAP[opkey]
                    part_key, thresh = condition.split(opkey)
                    condf = apply_rule(part_key, thresh, op, action)
                    workflows[name].append(condf)
                    break
        else:
            workflows[name].append(constantly(rparts[0]))

for part in parts:
    stack = ["in"]
    while stack:
        wf_key = stack.pop()
        for i, f in enumerate(workflows[wf_key]):
            res = f(part)
            if res:
                stack.append(res)
                break

print(sum(p.x + p.m + p.a + p.s for p in A))
