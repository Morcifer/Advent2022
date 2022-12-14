import itertools
from functools import partial, cmp_to_key
from typing import List, Optional, Tuple, Dict, Set

from src.utilities import load_data

DAY = 14


def flatten(sequence):
    return list(itertools.chain(*sequence))


def parser(s: List[str]) -> List[Tuple[int, int]]:
    path = []
    for i in range(0, len(s), 2):
        x, y = [int(n) for n in s[i].split(",")]
        path.append((x, y))

    return path


source_of_sand = (500, 0)


def process_data(data: List[List[Tuple[int, int]]], there_is_floor: bool) -> Set[Tuple[int, int]]:
    # Prepare map:
    stones = set()
    min_x, max_x = min([x for x, y in flatten(data)]),  max([x for x, y in flatten(data)])
    min_y, max_y = 0, max([y for x, y in flatten(data)])

    if there_is_floor:
        min_x, max_x = float('-inf'), float('inf')
        max_y = max_y + 2

    if there_is_floor:
        max_triangle_height = max_y + 1
        data.append(
            [
                (source_of_sand[0] - max_triangle_height, max_y),
                (source_of_sand[0] + max_triangle_height, max_y)
            ]
        )

    for path in data:
        for (x1, y1), (x2, y2) in zip(path[:-1], path[1:]):
            if x1 != x2 and y1 != y2:
                raise ValueError("Something might be off with the input!")

            if x1 == x2:
                range_y = range(y1, y2 + 1) if y1 < y2 else range(y1, y2 - 1, -1)
                for y in range_y:
                    stones.add((x1, y))
            else:
                range_x = range(x1, x2 + 1) if x1 < x2 else range(x1, x2 - 1, -1)
                for x in range_x:
                    stones.add((x, y1))

    everything = stones.copy()

    # Start dropping in sand
    stopped_sand = set()
    old_stopped_sand = -1
    sand_x, sand_y = 0, 0

    while len(stopped_sand) > old_stopped_sand and (sand_x, sand_y) != source_of_sand:  # Drop in sand
        old_stopped_sand = len(stopped_sand)
        sand_x, sand_y = source_of_sand

        while min_x <= sand_x <= max_x and min_y <= sand_y <= max_y:
            # still moving
            if (sand_x, sand_y + 1) not in everything:  # Down
                sand_x, sand_y = sand_x, sand_y + 1
            elif (sand_x - 1, sand_y + 1) not in everything:  # Down and to the left
                sand_x, sand_y = sand_x - 1, sand_y + 1
            elif (sand_x + 1, sand_y + 1) not in everything:  # Down and to the right
                sand_x, sand_y = sand_x + 1, sand_y + 1
            else:
                # print(f"Sand stopped at ({sand_x}, {sand_y})")
                stopped_sand.add((sand_x, sand_y))
                everything.add((sand_x, sand_y))

                break

    return stopped_sand


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, there_is_floor=False)
    return len(result)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, there_is_floor=True)
    return len(result)


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
