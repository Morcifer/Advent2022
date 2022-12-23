import itertools
import math
from collections import Counter
from copy import deepcopy
from functools import partial, cmp_to_key
from typing import List, Optional, Tuple, Dict, Set

from src.utilities import load_data

DAY = 23


def flatten(sequence):
    return list(itertools.chain(*sequence))


def parser(s: List[str]) -> str:
    return s[0]


def process_data(data: List[str], turns: int) -> int:
    elves = []
    for y, row in enumerate(data):
        for x, character in enumerate(row):
            if character == "#":
                elves.append((x, y))

#     If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
#     If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
#     If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
#     If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
    directions = [  # dx, dy
        ("N", (0, -1)),
        ("S", (0, 1)),
        ("W", (-1, 0)),
        ("E", (1, 0)),
    ]
    neighbours = {
        "N": [(0, -1), (-1, -1), (1, -1)],
        "S": [(0, 1), (-1, 1), (1, 1)],
        "W": [(-1, 0), (-1, -1), (-1, 1)],
        "E": [(1, 0), (1, -1), (1, 1)],
    }

    for turn in range(turns):
        new_elves = []

        # Part 1: Find spot to go to
        for elf_x, elf_y in elves:
            for direction, (direction_dx, direction_dy) in directions:
                for neighbour_dx, neighbour_dy in neighbours[direction]:
                    if (elf_x + neighbour_dx, elf_y + neighbour_dy) not in elves:
                        new_elves.append((elf_x + direction_dx, elf_y + direction_dy))

        # Part 2: Go to, if unoccupied
        new_elves_counter = Counter(new_elves)
        new_new_elves = []

        for old_elf, new_elf in zip(elves, new_elves):
            if new_elves_counter[new_elf] == 1:
                new_new_elves.append(new_elf)
            else:
                new_new_elves.append(old_elf)

        elves = new_new_elves

        # Part 3: iterate the directions
        first_direction = directions.pop(0)
        directions.append(first_direction)

    # At the very end:
    max_x, min_x = max(x for x, y in elves), min(x for x, y in elves)
    max_y, min_y = max(y for x, y in elves), min(y for x, y in elves)

    return (max_x - min_x) * (max_y - min_y) - len(elves)


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, turns=10)
    return result


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, turns=10)
    return result


if __name__ == '__main__':
    is_test = True
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
