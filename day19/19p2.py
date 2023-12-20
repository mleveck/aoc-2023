import dataclasses
from collections import defaultdict
from operator import gt, lt
from functools import partial
from util import *
from dataclasses import dataclass
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

wftxt, partstxt = input.split("\n\n")

OPMAP = {">": gt, "<": lt}


@dataclass
class PartR:
    x: tuple[int, int]
    m: tuple[int, int]
    a: tuple[int, int]
    s: tuple[int, int]


A: list[PartR] = []
R: list[PartR] = []
parts = []
workflows = defaultdict(list)


def place(bin, part):
    if bin == "A":
        A.append(part)
        return False, False, False
    if bin == "R":
        R.append(part)
        return False, False, False
    assert False


def apply_rule(part_key, thresh, op, next_wf):
    def rule(part):
        old_val = getattr(part, part_key)
        new_vali = None
        new_vale = None
        if op == ">":
            new_vali = (int(thresh) + 1, old_val[1])
            new_vale = (old_val[0], int(thresh))
        if op == "<":
            new_vali = (old_val[0], int(thresh) - 1)
            new_vale = (int(thresh), old_val[1])
        if not new_vali or not new_vale:
            print(part, part_key, op, next_wf, thresh)
            exit(1)
        if new_vali[0] > new_vali[1]:
            new_vali = None
        if new_vale[0] > new_vale[1]:
            new_vali = None
        new_partri = dataclasses.replace(partr)
        new_partre = dataclasses.replace(partr)
        setattr(new_partri, part_key, new_vali)
        new_partre = dataclasses.replace(partr)
        setattr(new_partre, part_key, new_vale)
        return next_wf, new_partri, new_partre

    return rule


def constantly(v):
    return lambda p: (v, p, False)


workflows["A"] = [partial(place, "A")]
workflows["R"] = [partial(place, "R")]

for line in wftxt.splitlines():
    name, rest = line.split("{")
    rest = rest.strip("}")
    rules = rest.split(",")
    for rule in rules:
        rparts = rule.split(":")
        if len(rparts) == 2:
            condition, next_wf = rparts[0], rparts[1]
            for opkey in OPMAP.keys():
                if opkey in condition:
                    op = OPMAP[opkey]
                    part_key, thresh = condition.split(opkey)
                    condf = apply_rule(part_key, thresh, opkey, next_wf)
                    workflows[name].append(condf)
                    break
        else:
            workflows[name].append(constantly(rparts[0]))

stack = [("in", PartR((1, 4000), (1, 4000), (1, 4000), (1, 4000)))]
while stack:
    wf_key, partr = stack.pop()
    for i, f in enumerate(workflows[wf_key]):
        wfk, resi, rese = f(partr)
        if resi:
            stack.append((wfk, resi))
        if rese:
            partr = rese
        else:
            break

combo_count = 0
for partr in A:
    combop = (
        ((partr.x[1] - partr.x[0]) + 1)
        * ((partr.m[1] - partr.m[0]) + 1)
        * ((partr.a[1] - partr.a[0]) + 1)
        * ((partr.s[1] - partr.s[0]) + 1)
    )
    combo_count += combop

print(combo_count)
