from typing import List
from collections import namedtuple
from util import *
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

lines = input.splitlines()

Pattern = namedtuple("Pattern", "rows cols")
patterns_txt = psplitdlines(s=input)

patterns = []
for pattern_txt in patterns_txt:
    rows = tuple(tuple(line) for line in pattern_txt.splitlines())
    cols = tuple(zip(*rows))
    patterns.append(Pattern(rows, cols))


def is_reflect_idx(r_idx: int, collection: List[tuple[str, ...]]) -> bool:
    l_idx = r_idx - 1
    smudge_cnt = 0
    while l_idx > -1 and r_idx < len(collection):
        if collection[r_idx] != collection[l_idx]:
            if 1 != sum(
                [
                    0 if el1 == el2 else 1
                    for el1, el2 in zip(collection[r_idx], collection[l_idx])
                ]
            ):
                return False
            smudge_cnt += 1
        r_idx += 1
        l_idx -= 1
    return smudge_cnt == 1


row_reflections = []
col_reflections = []
for pattern in patterns:
    for i in range(1, len(pattern.rows)):
        if is_reflect_idx(i, pattern.rows):
            row_reflections.append(i)
            break
    for i in range(1, len(pattern.cols)):
        if is_reflect_idx(i, pattern.cols):
            col_reflections.append(i)
            break

print(sum(col_reflections) + 100 * sum(row_reflections))
