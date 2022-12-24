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


def process_data(data: List[str]) -> int:
    blizzards = []

    for y, row in enumerate(data):
        for x, character in enumerate(row):
            if character in [">", "<", "^", "v"]:
                blizzards.append((x, y, character))

    directions = {
        "^": (0, -1),
        "v": (0, 1),
        "<": (-1, 0),
        ">": (1, 0),
    }

    height = len(data)
    width = len(data[0])

    entrance = (1, 0)
    exit = (width - 2, height - 1)

    to_search = [(0, entrance, blizzards.copy())]

    while len(to_search) > 0:
        minute, (spot_x, spot_y), blizzards = to_search.pop(0)

        print(f"Exploring minute {minute} where we're in ({spot_x}, {spot_y})")

        # Update blizzards to know where to go.
        new_blizzards = []

        for blizzard_x, blizzard_y, blizzard_direction in blizzards:
            dx, dy = directions[blizzard_direction]
            new_x, new_y = blizzard_x + dx, blizzard_y + dy

            if new_x == 0:
                new_x = width - 2
            if new_x == width - 1:
                new_x = 1

            if new_y == 0:
                new_y = height - 2
            if new_y == height - 1:
                new_y = 1

            new_blizzards.append((new_x, new_y, blizzard_direction))

        new_blizzards_spots = set((x, y) for x, y, _ in new_blizzards)

        # Wait
        if (spot_x, spot_y) not in new_blizzards_spots:
            to_search.append((minute + 1, (spot_x, spot_y), new_blizzards.copy()))

        # Move
        for dx, dy in directions.values():
            if (spot_x + dx, spot_y + dy) == exit:
                return minute + 1

            if (spot_y + dy, spot_x + dx) != entrance \
                    and 1 <= spot_x + dx <= width - 2 \
                    and 1 <= spot_y + dy <= height - 2 \
                    and (spot_x + dx, spot_y + dy) not in new_blizzards_spots:
                to_search.append((minute + 1, (spot_x + dx, spot_y + dy), new_blizzards.copy()))

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
