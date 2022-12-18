import itertools
import math
from copy import deepcopy
from functools import partial, cmp_to_key
from typing import List, Optional, Tuple, Dict, Set

from src.utilities import load_data

DAY = 18


def flatten(sequence):
    return list(itertools.chain(*sequence))


def parser(s: List[str]) -> Tuple[int, int, int]:
    return tuple(int(x) for x in s[0].split(","))


three_dimensional_neighbours = [
    (0, 0, 1),
    (0, 0, -1),
    (0, 1, 0),
    (0, -1, 0),
    (1, 0, 0),
    (-1, 0, 0),
]


def process_data(data: List[Tuple[int, int, int]]) -> int:
    droplets = set(data)
    surface_area = 6 * len(droplets)

    for x, y, z in droplets:
        for dx, dy, dz in three_dimensional_neighbours:
            if (x + dx, y + dy, z + dz) in droplets:
                surface_area -= 1

    return surface_area


def process_data_2(data: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    droplets = set(data)

    # Now how do I find holes?
    min_x, max_x = min(x for x, y, z in droplets), max(x for x, y, z in droplets)
    min_y, max_y = min(y for x, y, z in droplets), max(y for x, y, z in droplets)
    min_z, max_z = min(z for x, y, z in droplets), max(z for x, y, z in droplets)

    # Floodfill from a point outside, then count the cubes that are not in droplets and also not in flood.
    still_to_flood = {(min_x - 1, min_y - 1, min_z - 1)}
    flooded = set()

    while len(still_to_flood) > 0:
        to_flood_now = still_to_flood.pop()

        if to_flood_now in droplets:
            continue

        if to_flood_now in flooded:
            continue

        flooded.add(to_flood_now)

        x, y, z = to_flood_now

        if not (min_x - 1 <= x <= max_x + 1):
            continue

        if not (min_y - 1 <= y <= max_y + 1):
            continue

        if not (min_z - 1 <= z <= max_z + 1):
            continue

        for dx, dy, dz in three_dimensional_neighbours:
            still_to_flood.add((x + dx, y + dy, z + dz))

    # At this point we will have a list of all flooded cubes. If a cube is in neither set, it's a hole
    holes = []

    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            for z in range(min_z - 1, max_z + 2):
                this = x, y, z
                if this not in droplets and this not in flooded:
                    holes.append(this)

    return holes


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    return result


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    all_surface_area = process_data(data)
    internal_cubes = process_data_2(data)
    internal_surface_area = process_data(internal_cubes)

    return all_surface_area - internal_surface_area


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
