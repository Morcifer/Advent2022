import itertools
import math
from collections import Counter
from copy import deepcopy
from functools import partial, cmp_to_key
from typing import List, Optional, Tuple, Dict, Set

from src.utilities import load_data

DAY = 24


def flatten(sequence):
    return list(itertools.chain(*sequence))


def parser(s: List[str]) -> str:
    return s[0]


def draw_blizzards_on_map(elves):
    max_x, min_x = max(x for x, y in elves), min(x for x, y in elves)
    max_y, min_y = max(y for x, y in elves), min(y for x, y in elves)

    elves_to_draw = [(x - min_x, y - min_y) for x, y in elves]

    map = [
        "".join("#" if (x, y) in elves_to_draw else "." for x in range(0, max_x - min_x + 1))
        for y in range(0, max_y - min_y + 1)
    ]

    for row in map:
        print(row)


class BlizzardHandler:
    def __init__(self, blizzards, width, height):
        self.width = width
        self.height = height

        self.split_blizzards = {
            "^": {0: []},
            "v": {0: []},
            "<": {0: []},
            ">": {0: []},
        }

        for x, y, direction in blizzards:
            self.split_blizzards[direction][0].append((x, y))

        for minute in range(1, width - 2):
            # Right
            previous_minute = self.split_blizzards[">"][minute - 1]
            self.split_blizzards[">"][minute] = [(1 if x == width - 2 else x + 1, y) for (x, y) in previous_minute]

            # Left
            previous_minute = self.split_blizzards["<"][minute - 1]
            self.split_blizzards["<"][minute] = [(width - 2 if x == 1 else x - 1, y) for (x, y) in previous_minute]

        for minute in range(1, height - 2):
            # Up
            previous_minute = self.split_blizzards["^"][minute - 1]
            self.split_blizzards["^"][minute] = [(x, height - 2 if y == 1 else y - 1) for (x, y) in previous_minute]

            # Left
            previous_minute = self.split_blizzards["v"][minute - 1]
            self.split_blizzards["v"][minute] = [(x, 1 if y == height - 2 else y + 1) for (x, y) in previous_minute]

    def is_blizzard_in_spot_on_minute(self, minute, spot):
        rights = self.split_blizzards[">"][minute % (self.width - 2)]
        lefts = self.split_blizzards["<"][minute % (self.width - 2)]
        ups = self.split_blizzards["^"][minute % (self.height - 2)]
        downs = self.split_blizzards["v"][minute % (self.height - 2)]

        return spot in rights or spot in lefts or spot in ups or spot in downs


def process_data(data: List[str]) -> int:
    height = len(data)
    width = len(data[0])

    blizzards = []

    for y, row in enumerate(data):
        for x, character in enumerate(row):
            if character in [">", "<", "^", "v"]:
                blizzards.append((x, y, character))

    blizzard_handler = BlizzardHandler(blizzards, width, height)

    neighbours = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    entrance = (1, 0)
    exit = (width - 2, height - 1)

    to_search = [(0, entrance[0], entrance[1])]

    while len(to_search) > 0:
        minute, spot_x, spot_y = to_search.pop(0)

        print(f"Exploring minute {minute} where we're in ({spot_x}, {spot_y})")

        # Wait
        if not blizzard_handler.is_blizzard_in_spot_on_minute(minute + 1, spot=(spot_x, spot_y)):
            to_search.append((minute + 1, spot_x, spot_y))

        # Move
        for dx, dy in neighbours:
            if (spot_x + dx, spot_y + dy) == exit:
                return minute + 1

            if (spot_y + dy, spot_x + dx) != entrance \
                    and 1 <= spot_x + dx <= width - 2 \
                    and 1 <= spot_y + dy <= height - 2 \
                    and not blizzard_handler.is_blizzard_in_spot_on_minute(minute + 1, spot=(spot_x + dx, spot_y + dy)):
                to_search.append((minute + 1, spot_x + dx, spot_y + dy))

    return -1


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    return result


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    return result


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    # print(f"Day {DAY} result 2: {part_2(is_test)}")
