import itertools
import math
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
        (bottom_left_x + 1, bottom_left_y + 1),
        (bottom_left_x + 2, bottom_left_y + 1),
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
        # print(f"Height {i}: {''.join(chamber[i])}")
        print(''.join(chamber[i]))

    print("")


fixed_floor = [c for c in "-------"]
fixed_empty = [c for c in "......."]


def process_data(data: str, stopped_rocks) -> Tuple[List[List[str]], List[Tuple[int, int]]]:
    chamber = [fixed_floor[:]]
    gust_turn_and_height_per_rock_turn = []

    gust_turn = 0

    for rock_turn in range(stopped_rocks):
        print(f"Rock turn {rock_turn + 1} out of {stopped_rocks}")
        # print_chamber(chamber, None)

        max_height = 1 + max(
            y
            for y in range(len(chamber))
            if any(chamber[y][x] != "." for x in range(WIDTH))
        )

        gust_turn_and_height_per_rock_turn.append((gust_turn, max_height - 1))

        # New rock appears!
        new_rock = rock_dictionary[rock_turn % 5](max_height)
        max_y = max(y for x, y in new_rock)
        height_difference = max_y - len(chamber) + 1
        chamber.extend([fixed_empty[:] for _ in range(height_difference)])

        # print_chamber(chamber, None)
        # print_chamber(chamber, new_rock)

        # Rock keeps moving!
        while True:
            # Move by gust!
            gust = data[gust_turn % len(data)]
            gust_turn += 1

            if gust == "<":
                min_x = min(x for x, y in new_rock)
                possible_new_rock = [(x - 1, y) for x, y in new_rock]
                if min_x >= 1:
                    can_move = True
                    for x, y in possible_new_rock:
                        if chamber[y][x] != ".":
                            can_move = False
                            break
                    if can_move:
                        # print("GO LEFT!")
                        new_rock = possible_new_rock
            else:
                max_x = max(x for x, y in new_rock)
                possible_new_rock = [(x + 1, y) for x, y in new_rock]
                if max_x < WIDTH - 1:
                    can_move = True
                    for x, y in possible_new_rock:
                        if chamber[y][x] != ".":
                            can_move = False
                            break
                    if can_move:
                        # print("GO RIGHT!")
                        new_rock = possible_new_rock

            # print_chamber(chamber, new_rock)

            keep_falling = True

            for x, y in new_rock:
                if chamber[y - 1][x] != ".":
                    keep_falling = False
                    break

            if keep_falling:
                new_rock = [(x, y - 1) for x, y in new_rock]
                # print("KEEP FALLING!")
                # print_chamber(chamber, new_rock)
            else:
                for x, y in new_rock:
                    chamber[y][x] = str(rock_turn % 5)

                # print("ROCK STOPPED!")
                # print_chamber(chamber, None)
                break

    print_chamber(chamber, None)

    max_height = 1 + max(
        y
        for y in range(len(chamber))
        if any(chamber[y][x] != "." for x in range(WIDTH))
    )

    gust_turn_and_height_per_rock_turn.append((gust_turn, max_height - 1))

    return chamber, gust_turn_and_height_per_rock_turn


def find_periodicity(chamber, gust_turn_and_height_per_rock_turn, length_of_gusts) -> Tuple[int, int, int, int]:
    # start, periodicity, extra
    print(gust_turn_and_height_per_rock_turn)
    diffs_of_heights_per_gust_turn = [
        (gust_turn_2 - gust_turn_1, height_2 - height_1)
        for (gust_turn_1, height_1), (gust_turn_2, height_2)
        in zip(gust_turn_and_height_per_rock_turn[:-1], gust_turn_and_height_per_rock_turn[1:])
    ]
    print(diffs_of_heights_per_gust_turn)
    print("???")

    minimum_gust_turn_periodicity = length_of_gusts * len(rock_dictionary)

    for rock_turn_periodicity in range(5, minimum_gust_turn_periodicity * 5, 5):
        print(f"Trying to check rock turn periodicity of {rock_turn_periodicity}")

        for starting_rock_turn in range(
            0,
            min(minimum_gust_turn_periodicity * 3, len(gust_turn_and_height_per_rock_turn) - rock_turn_periodicity - 1),
            1
        ):
            this = diffs_of_heights_per_gust_turn[starting_rock_turn:starting_rock_turn + rock_turn_periodicity]
            next = diffs_of_heights_per_gust_turn[starting_rock_turn + rock_turn_periodicity: starting_rock_turn + rock_turn_periodicity + rock_turn_periodicity]

            total_gust_turns = sum(turn for turn, height in this)
            total_height = sum(height for turn, height in this)

            if total_gust_turns % length_of_gusts != 0:
                print(f"Height {total_height} in {total_gust_turns} gust turns "
                      f"when starting at {starting_rock_turn} for periodicity {rock_turn_periodicity} "
                      f"is not multiple of {length_of_gusts}. Continuing.")
                continue

            if this == next:
                print(
                    f"Found possible periodicity! "
                    f"It starts at {starting_rock_turn} with rock periodicity {rock_turn_periodicity} "
                    f"and has height {total_height} after {total_gust_turns} gust turns!"
                )

                starting_gust_turn, starting_height = gust_turn_and_height_per_rock_turn[starting_rock_turn]

                valid = True

                for height in range(starting_height + 1, starting_height + total_height + 1):
                    if chamber[height] != chamber[height + total_height]:
                        valid = False
                        break

                if valid:
                    return starting_rock_turn, rock_turn_periodicity, total_height, total_gust_turns
                else:
                    print(f"Validation failed at heights {height} and {height + total_height}. Keep checking.")

    print("I failed at finding periodicity. Maybe increase the size?")
    return None


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    chamber, height_per_gust_turn = process_data(data[0], stopped_rocks=2022)
    return height_per_gust_turn[-1][1]


def part_2(is_test: bool) -> int:
    rock_turn_max_value = 1000000000000

    data = load_data(DAY, parser, "data", is_test=is_test)
    length_of_gusts = len(data[0])
    chamber, gust_turn_and_height_per_rock_turn = process_data(data[0], stopped_rocks=2022 if is_test else 5000)

    starting_rock_turn, rock_turn_periodicity, total_height, total_gust_turns = find_periodicity(chamber, gust_turn_and_height_per_rock_turn, length_of_gusts)

    height_until_periodicity_starts = gust_turn_and_height_per_rock_turn[starting_rock_turn][1]
    print(f"Height until periodicity starts: {height_until_periodicity_starts}")

    number_of_rock_periods = math.floor((1.0 * rock_turn_max_value - starting_rock_turn) / rock_turn_periodicity)
    height_after_periodicity_ends = height_until_periodicity_starts + number_of_rock_periods * total_height

    print(f"Height after periodicity ends: {height_after_periodicity_ends}")

    remaining_rock_turns = rock_turn_max_value - starting_rock_turn - number_of_rock_periods * rock_turn_periodicity
    print(f"remaining_turns: {remaining_rock_turns}")

    starting_remainder = gust_turn_and_height_per_rock_turn[starting_rock_turn]
    end_remainder = gust_turn_and_height_per_rock_turn[starting_rock_turn + remaining_rock_turns]

    print(f"starting_remainder: {starting_remainder}")
    print(f"end_remainder: {end_remainder}")

    extra_height = end_remainder[1] - starting_remainder[1]
    print(f"extra_height: {extra_height}")

    height_after_extra = height_after_periodicity_ends + extra_height
    print(f"height_after_extra: {height_after_extra}")

    return height_after_extra  # Should be 3068 for 2022 and 1514285714288 for 1000000000000


if __name__ == '__main__':
    is_test = False
    # print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
