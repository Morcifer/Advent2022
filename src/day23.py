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


def draw_elves_on_map(elves):
    max_x, min_x = max(x for x, y in elves), min(x for x, y in elves)
    max_y, min_y = max(y for x, y in elves), min(y for x, y in elves)

    elves_to_draw = [(x - min_x, y - min_y) for x, y in elves]

    map = [
        "".join("#" if (x, y) in elves_to_draw else "." for x in range(0, max_x - min_x + 1))
        for y in range(0, max_y - min_y + 1)
    ]

    for row in map:
        print(row)


def process_data(data: List[str], turns: int, break_at_no_movement) -> int:
    elves = []
    for y, row in enumerate(data):
        for x, character in enumerate(row):
            if character == "#":
                elves.append((x, y))

    elves_set = set(elves)

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
        elf_needs_to_move = []

        # Part 1: Find spot to go to
        for elf_x, elf_y in elves:
            move_needed = False
            for side_dx, side_dy in set(flatten(neighbours.values())):
                if (elf_x + side_dx, elf_y + side_dy) in elves_set:
                    move_needed = True
                    elf_needs_to_move.append(True)
                    break

            if not move_needed:
                new_elves.append((elf_x, elf_y))
                elf_needs_to_move.append(False)
                continue

            move_allowed = False

            for direction, (direction_dx, direction_dy) in directions:
                direction_allowed = True
                for neighbour_dx, neighbour_dy in neighbours[direction]:
                    if (elf_x + neighbour_dx, elf_y + neighbour_dy) in elves_set:
                        direction_allowed = False
                        break

                if direction_allowed:
                    # print(f"The elf in ({elf_x}, {elf_y}) wants to go {direction}")
                    new_elves.append((elf_x + direction_dx, elf_y + direction_dy))
                    move_allowed = True
                    break

            if not move_allowed:
                new_elves.append((elf_x, elf_y))

        if all(not need_to_move for need_to_move in elf_needs_to_move):
            return turn + 1

        # Part 2: Go to, if unoccupied
        new_elves_counter = Counter(new_elves)
        new_new_elves = []

        for old_elf, new_elf in zip(elves, new_elves):
            if new_elves_counter[new_elf] == 1:
                new_new_elves.append(new_elf)
            else:
                new_new_elves.append(old_elf)

        elves = new_new_elves
        elves_set = set(elves)

        # Part 3: iterate the directions
        first_direction = directions.pop(0)
        directions.append(first_direction)

    # At the very end:
    max_x, min_x = max(x for x, y in elves), min(x for x, y in elves)
    max_y, min_y = max(y for x, y in elves), min(y for x, y in elves)

    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, turns=10, break_at_no_movement=False)
    return result


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, turns=1000, break_at_no_movement=True)  # Between 800 and 1000.
    return result


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
