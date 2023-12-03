from util import *
from dataclasses import dataclass
import string
from collections import *
from itertools import *
from functools import *
from operator import *


input = slurp("input.txt")
sample = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

sline = "467..114.."

def proc_line(l: str):
    return list(l)

proc_sample = psplitlines(proc_line, sample)
proc_input = psplitlines(proc_line, input)

def solve(grid):
    numbers = set((row, col) for row in range(len(grid))\
            for col in range(len(grid[0])) if grid[row][col].isdigit())
    symbols = set((row, col) for row in range(len(grid))\
            for col in range(len(grid[0])) if not grid[row][col].isdigit() and grid[row][col] != ".")

    actual_numbers = []
    visited = set()
    for s in symbols:
        pneighbors = potential_neighbors(s[0], s[1], grid)
        for pneighbor in pneighbors:
            if pneighbor in numbers and not pneighbor in visited:
                r, c = pneighbor[0], pneighbor[1]
                digits = grid[r][c]
                cprime = c - 1
                while (cprime >=0 and grid[r][cprime].isdigit()):
                    digits = grid[r][cprime] + digits
                    visited.add((r, cprime))
                    cprime -= 1
                cprime = c + 1
                while (cprime < len(grid[0]) and grid[r][cprime].isdigit()):
                    digits = digits + grid[r][cprime] 
                    visited.add((r, cprime))
                    cprime += 1
                actual_numbers.append(int(digits))
    return sum(actual_numbers)
solve(proc_sample) # 4361
solve(proc_input) # 532445
