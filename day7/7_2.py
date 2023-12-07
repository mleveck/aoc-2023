from typing import Tuple
from enum import IntEnum
from operator import mul
from collections import Counter
from functools import cmp_to_key
from itertools import starmap
from util import *
import sys

if len(sys.argv) > 1:
    input = open(sys.argv[1]).read().strip()
else:
    input = open("./sample.txt").read().strip()

lines = input.splitlines()

cards = {
    c: (i + 1)
    for i, c in enumerate(reversed("A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J".split(", ")))
}


class HandType(IntEnum):
    highcard = 1
    pair = 2
    twopair = 3
    threekind = 4
    fhouse = 5
    fourkind = 6
    fivekind = 7


def cardtotype(card: str):
    counter = Counter(card)
    nj = counter.get("J", 0)
    if nj == 5:
        return HandType.fivekind
    if nj > 0:
        counter.pop("J")
    scardcount = [c[1] for c in counter.most_common()]
    if nj > 0:
        scardcount[0] = scardcount[0] + nj
    if scardcount[0] == 5:
        return HandType.fivekind
    if scardcount[0] == 4:
        return HandType.fourkind
    if scardcount[0] == 3:
        if scardcount[1] == 2:
            return HandType.fhouse
        return HandType.threekind
    if scardcount[0] == 2:
        if scardcount[1] == 2:
            return HandType.twopair
        return HandType.pair
    return HandType.highcard


def compare(a_play: Tuple[str, int], b_play: Tuple[str, int]):
    a_hand, b_hand = a_play[0], b_play[0]
    handtype_a, handtype_b = cardtotype(a_hand), cardtotype(b_hand)
    if handtype_a > handtype_b:
        return 1
    if handtype_a < handtype_b:
        return -1
    for card_a, card_b in zip(a_hand, b_hand):
        if cards[card_a] < cards[card_b]:
            return -1
        if cards[card_a] > cards[card_b]:
            return 1
    return 0


hands = []

for l in lines:
    h, b = l.split()
    hands.append((h, int(b)))

sorted_hands = sorted(hands, key=cmp_to_key(compare))

ranked_hands = [(i + 1, b) for i, (_, b) in enumerate(sorted_hands)]
sol = sum(starmap(mul, ranked_hands))

print(sol)
