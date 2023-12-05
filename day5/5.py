import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()


seeds_txts = input.split("\n\n")[0].split(": ")[1].split()
seeds = [int(s) for s in seeds_txts]


def parse_table(table: str):
    rows = table.splitlines()[1:]
    rows = [[int(col) for col in row.split()] for row in rows]
    return rows


def table_map(table):
    return {
        range(source, source + r): range(dest, dest + r) for dest, source, r in table
    }


tables = input.split("\n\n")[1:]
table_maps = [table_map(parse_table(t)) for t in tables]

locations = []
for s in seeds:
    key = s
    for tm in table_maps:
        for krange in tm:
            if key in krange:
                key = tm[krange].start + (key - krange.start)
                break
    locations.append(key)

print(min(locations))  # answer for part 1
# sample 35
# input 910845529
