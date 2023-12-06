import sys

sys.set_int_max_str_digits(500000)
if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

lines = input.splitlines()

table = [l.split(":")[1].strip().split() for l in lines]
race = [int("".join(r)) for r in table] 


time, dist = race
l, r = 0, time -1
m = (r - l)//2 + l

while l < r:
    m = (r - l)//2 + l
    if (time - m)*m > dist:
        r = m
    else:
        l = m + 1

tmin = m

l, r = 0, time -1
m = (r - l)//2 + l

while l < r:
    m = (r - l)//2 + l
    if (time - m)*m > dist:
        l = m + 1
    else:
        r = m 

tmax = m

print(tmax - tmin + 1)



