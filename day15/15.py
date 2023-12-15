from util import *
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

lines = input.splitlines()

instructions = lines[0].split(",")


def hash(s):
    code = 0
    for c in s:
        code += ord(c)
        code = code * 17
        code = code % 256
    return code


codes = [hash(inst) for inst in instructions]
print(sum(codes))
