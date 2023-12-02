from util import *
import string
from collections import *
from itertools import *


input = slurp("input.txt")

sample = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""


def parseline(l: str):
    digits = [c for c in l if c.isdigit()]
    return int(digits[0] + digits[-1])


sum(psplitlines(parseline, sample)) # 142
sum(psplitlines(parseline, input)) # 54940

sample2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

digits = "zero one two three four five six seven eight nine".split()


def parseline2(line: str):
    found_digits = []
    for line_idx, char in enumerate(line):
        for digit_idx in range(10):
            if (
                char == string.digits[digit_idx]
                or line[line_idx:].startswith(digits[digit_idx])
            ):
                found_digits.append(digit_idx)
                break
    first_digit, last_digit = found_digits[0], found_digits[-1]
    return first_digit * 10 + last_digit


sum(psplitlines(parseline2, sample2)) # 281
sum(psplitlines(parseline2, input)) # 54208
