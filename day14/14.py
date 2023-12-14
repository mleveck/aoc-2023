from typing import Counter
from util import *
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

lines = input.splitlines()

grid = parse_matrix(s=input, col_sep="")
cols = [list(c) for c in zip(*grid)]

for col in cols:
    for j, val in enumerate(col):
        if val == "O":
            i = j
            while i > 0:
                if col[i] == "O" and col[i - 1] == ".":
                    col[i], col[i - 1] = ".", "O"
                else:
                    break
                i -= 1

new_rows = list(zip(*cols))

ans = 0
for i, r in enumerate(new_rows):
    c = Counter(r)
    n_rocks = c.get("O", 0)
    score = n_rocks * (len(new_rows) - i)
    ans += score
print(ans)
