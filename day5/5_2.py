from typing import List
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()


tables = input.split("\n\n")[1:]

seeds_txts = input.split("\n\n")[0].split(": ")[1].split()
seeds = [int(s) for s in seeds_txts]
seeds2 = []
for i in range(0, len(seeds), 2):
    seeds2.append(range(seeds[i], seeds[i] + seeds[i + 1]))


def parse_table(table: str):
    rows = table.splitlines()[1:]
    rows = [[int(col) for col in row.split()] for row in rows]
    return rows


def table_map(table):
    return {
        range(source, source + r): range(dest, dest + r) for dest, source, r in table
    }


table_maps = [table_map(parse_table(t)) for t in tables]


def get_exclusions(r: range, cands: List[range]):
    if not cands:
        return [r]
    assert all(c.start in r and c.stop - 1 in r for c in cands)
    start, stop = r.start, r.stop
    res = []
    scands = sorted([(c.start, c.stop) for c in cands])
    for sc in scands:
        if sc[0] > start:
            res.append((start, sc[0]))
        start = sc[1]
        if stop > scands[-1][1]:
            res.append((sc[1], stop))
    return [range(*r) for r in res]


def get_isxn_and_translation(sr, krs, tbl):
    isxns, translations = [], []
    for kr in krs:
        if sr.start in kr:
            start = sr.start
            stop = min(sr.stop, kr.stop)
            ir = range(start, stop)
            isxns.append(ir)
            translation = range(
                tbl[kr].start + (ir.start - kr.start),
                tbl[kr].start + (ir.stop - kr.start),
            )
            translations.append(translation)
        elif sr.stop in kr:
            stop = sr.stop
            start = max(sr.start, kr.start)
            ir = range(start, stop)
            isxns.append(ir)
            translation = range(
                tbl[kr].start + (ir.start - kr.start),
                tbl[kr].start + (ir.stop - kr.start),
            )
            translations.append(translation)
    return isxns, translations


locations2 = []
for osr in seeds2:
    seedranges = [osr]
    for tm in table_maps:
        new_keys = []
        for sr in seedranges:
            intersections, translations = get_isxn_and_translation(sr, tm.keys(), tm)
            exclusions = get_exclusions(sr, intersections)
            new_keys.extend(translations)
            new_keys.extend(exclusions)
        seedranges = new_keys
    locations2.extend(seedranges)

print(min(r.start for r in locations2))  # answer for part 2
# sample 46
# input 77435348
