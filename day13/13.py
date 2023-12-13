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
    cols = tuple(col for col in zip(*rows))
    patterns.append(Pattern(rows, cols))


def is_reflect_idx(r_idx: int, collection: List[tuple[str, ...]]) -> bool:
    l_idx = r_idx - 1
    while l_idx > -1 and r_idx < len(collection):
        if collection[r_idx] != collection[l_idx]:
            return False
        r_idx += 1
        l_idx -= 1
    return True


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
