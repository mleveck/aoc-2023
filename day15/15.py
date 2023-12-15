from util import *
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

lines = input.splitlines()

codes = lines[0].split(",")

anss = []
for code in codes:
    ans = 0
    for c in code:
        ans += ord(c)
        ans = ans*17
        ans = ans % 256
    anss.append(ans)

print( sum(anss) )
