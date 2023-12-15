from collections import OrderedDict
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


boxes = defaultdict(OrderedDict)

for inst in instructions:
    if (op_idx := inst.find("-")) != -1:
        label = inst[:op_idx]
        box = hash(label)
        if label in boxes[box]:
            boxes[box].pop(label)
    elif (op_idx := inst.find("=")) != -1:
        label, focal_len = inst[:op_idx], int(inst[op_idx + 1 :])
        box = hash(label)
        boxes[box][label] = focal_len

res = []
for i in range(256):
    power = i + 1
    box = boxes[i]
    for idx, (label, focal_len) in enumerate(box.items()):
        slot_num = idx + 1
        res.append(power * slot_num * focal_len)

print(sum(res))
