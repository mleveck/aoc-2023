from util import *
from dataclasses import dataclass
import string
from collections import *
from itertools import *
from functools import *
from operator import *


input = slurp("input.txt")

sample = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

Pair = namedtuple("Pair", "num color")


@dataclass
class Game:
    id: int
    draws: list[Pair]


def parseline(l: str):
    gid = int(l.split(":")[0].split(" ")[1])
    draws_txt = l.split(": ")[1].split("; ")
    draws = [
        Pair(int(pair[0]), pair[1])
        for pairs_txt in draws_txt
        for pair_txt in pairs_txt.split(", ")
        if len(pair := pair_txt.split(" ")) == 2
    ]
    return Game(gid, draws)


BAG = {"red": 12, "green": 13, "blue": 14}


def possible_game(g: Game) -> bool:
    for pair in g.draws:
        if pair.num not in range(BAG[pair.color] + 1):
            return False
    return True


def ans1(input_games):
    parsed = psplitlines(parseline, input_games)
    return sum(game.id for game in filter(possible_game, parsed))


ans1(sample) # 8
ans1(input)  # 2156


def power(g: Game):
    reds = [p.num for p in g.draws if p.color == "red"]
    greens = [p.num for p in g.draws if p.color == "green"]
    blues = [p.num for p in g.draws if p.color == "blue"]
    return reduce(mul, [max(reds), max(greens), max(blues)])


def ans2(input):
    return sum([power(g) for g in psplitlines(parseline, input)])


ans2(sample)  # 2286
ans2(input)  # 66909
