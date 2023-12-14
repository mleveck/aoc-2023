from typing import NamedTuple
from itertools import groupby
from functools import lru_cache
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
    broken_spring_counts = tuple(len(tuple(g)) for k, g in groupby(record) if k == "#")
    return chksum == broken_spring_counts


def plausible(r: str, chksum: tuple[int, ...]):
    substr = r
    for chknum in chksum:
        idx_wild = substr.find("?")
        idx_first_broken = substr.find("#")
        if idx_first_broken == -1:
            return True
        if idx_first_broken > idx_wild:
            return True
        for i in range(chknum):
            if substr[idx_first_broken + i] == "?":
                return True
            if substr[idx_first_broken + i] != "#":
                return False
        if not (
            idx_first_broken + chknum == len(substr)
            or substr[idx_first_broken + chknum] == "."
            or substr[idx_first_broken + chknum] == "?"
        ):
            return False
        substr = substr[idx_first_broken + chknum :]
    return True


def hard_satisfies(r: str, chknum: int):
    idx_wild = r.find("?")
    idx_first_broken = r.find("#")
    if idx_first_broken < idx_wild:
        for i in range(chknum):
            if i + idx_first_broken > len(r) - 1:
                return False
            if r[idx_first_broken + i] != "#":
                return False
        if idx_first_broken + chknum == len(r) or r[idx_first_broken + chknum] == ".":
            return True
    return False


@lru_cache(1024 * 128)
def backtrack(r: str, chksum: tuple[int, ...]) -> int:
    idx_wild = r.find("?")
    idx_first_broken = r.find("#")
    idx_last_broken = r[::-1].find("#")
    if idx_wild == -1 or not chksum:
        if validate(r, chksum):
            return 1
        return 0
    if hard_satisfies(r, chksum[0]):
        return backtrack(r[idx_first_broken + chksum[0] :], chksum[1:])
    if hard_satisfies(r[::-1], chksum[-1]):
        new_r = r[: -(idx_last_broken + chksum[-1])]
        new_chksum = chksum[:-1]
        return backtrack(new_r, new_chksum)
    if not plausible(r, chksum):
        return 0
    rbroken = r.replace("?", "#", 1)
    rworking = r.replace("?", ".", 1)
    return backtrack(rbroken, chksum) + backtrack(rworking, chksum)


for line in lines:
    rt, cst = line.split(" ")
    record_val = "?".join([rt] * 5)
    chksum_val = tuple(int(cs) for cs in cst.split(",")) * 5
    r = Record(record_val, chksum_val)
    records.append(r)

print(sum([backtrack(*r) for r in records]))
