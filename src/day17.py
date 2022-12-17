import itertools
from copy import deepcopy
from functools import partial, cmp_to_key
from typing import List, Optional, Tuple, Dict, Set

from src.utilities import load_data

DAY = 17


def flatten(sequence):
    return list(itertools.chain(*sequence))


def parser(s: List[str]) -> str:
    return s[0]


WIDTH = 7

# Each rock appears so that its left edge is two units away from the left wall
# and its bottom edge is three units above the highest rock in the room (or the floor, if there isn't one).


def rock_0(height_y) -> List[Tuple[int, int]]:
    # ####
    bottom_left_x, bottom_left_y = (2, height_y + 3)

    return [
        (bottom_left_x, bottom_left_y),
        (bottom_left_x + 1, bottom_left_y),
        (bottom_left_x + 2, bottom_left_y),
        (bottom_left_x + 3, bottom_left_y),
    ]


def rock_1(height_y) -> List[Tuple[int, int]]:
    # .#.
    # ###
    # .#.
    bottom_left_x, bottom_left_y = (2, height_y + 3)

    return [
        (bottom_left_x + 1, bottom_left_y),
        (bottom_left_x, bottom_left_y + 1),
        (bottom_left_x, bottom_left_y + 1),
        (bottom_left_x, bottom_left_y + 1),
        (bottom_left_x + 1, bottom_left_y + 2),
    ]


def rock_2(height_y) -> List[Tuple[int, int]]:
    # ..#
    # ..#
    # ###
    bottom_left_x, bottom_left_y = (2, height_y + 3)

    return [
        (bottom_left_x, bottom_left_y),
        (bottom_left_x + 1, bottom_left_y),
        (bottom_left_x + 2, bottom_left_y),
        (bottom_left_x + 2, bottom_left_y + 1),
        (bottom_left_x + 2, bottom_left_y + 2),
    ]


def rock_3(height_y) -> List[Tuple[int, int]]:
    # #
    # #
    # #
    # #
    bottom_left_x, bottom_left_y = (2, height_y + 3)
    return [
        (bottom_left_x, bottom_left_y),
        (bottom_left_x, bottom_left_y + 1),
        (bottom_left_x, bottom_left_y + 2),
        (bottom_left_x, bottom_left_y + 3),
    ]


def rock_4(height_y) -> List[Tuple[int, int]]:
    # ##
    # ##
    bottom_left_x, bottom_left_y = (2, height_y + 3)
    return [
        (bottom_left_x, bottom_left_y),
        (bottom_left_x + 1, bottom_left_y),
        (bottom_left_x, bottom_left_y + 1),
        (bottom_left_x + 1, bottom_left_y + 1),
    ]


rock_dictionary = {
    0: rock_0,
    1: rock_1,
    2: rock_2,
    3: rock_3,
    4: rock_4,
}


def print_chamber(chamber: List[List[str]], extra_rock):
    chamber = deepcopy(chamber)

    if extra_rock is not None:
        for x, y in extra_rock:
            chamber[y][x] = "@"

    for i in range(len(chamber) - 1, -1, -1):
        print("".join(chamber[i]))

    print("")


fixed_floor = [c for c in "-------"]
fixed_empty = [c for c in "......."]


def process_data(data: str) -> List[Tuple[int, str]]:
    chamber = [fixed_floor[:]]

    gust_turn = 0

    for rock_turn in range(2023):
        print_chamber(chamber, None)

        # New rock appears!
        new_rock = rock_dictionary[rock_turn % 5](len(chamber))
        max_y = max(y for x, y in new_rock)
        height_difference = max_y - len(chamber) + 1
        chamber.extend([fixed_empty[:] for _ in range(height_difference)])

        print_chamber(chamber, None)
        print_chamber(chamber, new_rock)

        # Rock keeps moving!
        while True:
            # Move by gust!
            gust = data[gust_turn % len(data)]
            gust_turn += 1

            if gust == "<":
                min_x = min(x for x, y in new_rock)
                if min_x >= 1:
                    print("GO RIGHT!")
                    new_rock = [(x - 1, y) for x, y in new_rock]
            else:
                max_x = max(x for x, y in new_rock)
                if max_x < WIDTH - 1:
                    print("GO LEFT!")
                    new_rock = [(x + 1, y) for x, y in new_rock]

            print_chamber(chamber, new_rock)

            keep_falling = True

            for x, y in new_rock:
                if chamber[y - 1][x] != ".":
                    keep_falling = False
                    break

            if keep_falling:
                new_rock = [(x, y - 1) for x, y in new_rock]
                print("KEEP FALLING!")
                print_chamber(chamber, new_rock)
            else:
                for x, y in new_rock:
                    chamber[y][x] = "#"

                print("ROCK STOPPED!")
                print_chamber(chamber, None)
                break

    return chamber


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data[0])
    return max(result, key=lambda c: c[0])[0]


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    all_options = process_data(data)
    return 0


if __name__ == '__main__':
    is_test = True
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    # print(f"Day {DAY} result 2: {part_2(is_test)}")
