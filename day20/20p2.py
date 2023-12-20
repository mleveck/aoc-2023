from typing import Deque, NamedTuple
from collections import deque
from dataclasses import dataclass
from util import *
import sys
import math

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./input.txt").read().strip()

NBUTTON_PUSHES = 1000


class Signal(NamedTuple):
    dest: str
    src: str
    high: bool


modules = []

signal_bus: Deque[Signal] = deque()


@dataclass
class Dummy:
    id: str
    dests: list[str]

    def process(self, signal: Signal):
        return None


@dataclass
class Broadcast:
    id: str
    dests: list[str]

    def process(self, signal: Signal):
        for dest in self.dests:
            signal_bus.append(Signal(dest, self.id, signal.high))


@dataclass
class FlipFlop:
    id: str
    dests: list[str]
    state: bool = False

    def process(self, signal: Signal):
        out = False
        if signal.high:
            return None
        if self.state:
            out = False
        else:
            out = True
        for dest in self.dests:
            signal_bus.append(Signal(dest, self.id, out))
        self.state = not self.state


@dataclass
class Conjunction:
    id: str
    dests: list[str]
    state: dict[str, bool]

    def process(self, signal: Signal):
        out = True
        self.state[signal.src] = signal.high
        if all(hl for _, hl in self.state.items()):
            out = False
        for dest in self.dests:
            signal_bus.append(Signal(dest, self.id, out))


module_map: dict[str, Broadcast | FlipFlop | Conjunction | Dummy] = {}

for line in input.splitlines():
    src, dsts = line.split(" -> ")
    dests = dsts.split(", ")
    if src == "broadcaster":
        module = Broadcast(id="broadcaster", dests=dests)
        module_map["broadcaster"] = module
    else:
        src_type = src[0]
        src_id = src[1:]
        if src_type == "%":
            module = FlipFlop(id=src_id, dests=dests)
            module_map[src_id] = module
        elif src_type == "&":
            state_map = dict()
            module = Conjunction(id=src_id, dests=dests, state=state_map)
            module_map[src_id] = module

for id, mod in module_map.items():
    for dest in mod.dests:
        if dest in module_map and isinstance(module_map[dest], Conjunction):
            module_map[dest].state[id] = False

cnin = (
    []
)  # this was the input to rx which is a conjunction box. We're gonna find it's inputs' cycles
for id, mod in module_map.items():
    if "cn" in mod.dests:
        cnin.append(mod.id)

bpresses = 0
cycles = dict()
while len(cycles.keys()) != len(cnin):
    bpresses += 1
    signal_bus.append(Signal(dest="broadcaster", src="button", high=False))
    while signal_bus:
        signal = signal_bus.popleft()
        if signal.src in cnin and signal.high and signal.src not in cycles:
            cycles[signal.src] = bpresses
        if signal.dest in module_map:
            module_map[signal.dest].process(signal)

print(math.lcm(*cycles.values()))
