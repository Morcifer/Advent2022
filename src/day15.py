import itertools
from functools import partial, cmp_to_key
from typing import List, Optional, Tuple, Dict, Set

from src.utilities import load_data

DAY = 15


def flatten(sequence):
    return list(itertools.chain(*sequence))


def parser(s: List[str]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    # Sensor at x=13, y=2: closest beacon is at x=15, y=3
    def get_int(substring):
        return int(substring.replace(",", "").replace(":", "").split("=")[1])

    return (get_int(s[2]), get_int(s[3])),  (get_int(s[8]), get_int(s[9]))


def manhattan_distance(point_1: Tuple[int, int], point_2: Tuple[int, int]) -> int:
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])


def process_data(data: List[Tuple[Tuple[int, int], Tuple[int, int]]], target_y: int) -> Set[Tuple[int, int]]:
    no_beacons = set()
    beacons = set(beacon for _, beacon in data)

    for i, (sensor, beacon) in enumerate(data):
        print(f"I'm at sensor {i} out of {len(data)}")
        distance = manhattan_distance(sensor, beacon)
        y = target_y
        for x in range(sensor[0] - distance, sensor[0] + distance + 1):
            if manhattan_distance(sensor, (x, y)) <= distance and (x, y) not in beacons:
                no_beacons.add((x, y))

    return no_beacons


def process_data_2(data: List[Tuple[Tuple[int, int], Tuple[int, int]]], max_value: int) -> Tuple[int, int]:
    sensor_beacon_distances = [
        (sensor, beacon, manhattan_distance(sensor, beacon))
        for (sensor, beacon) in data
    ]

    for x in range(0, max_value):
        print(f"I'm at x = {x}")

        for y in range(0, max_value):
            valid = True

            for sensor, beacon, distance in sensor_beacon_distances:
                if manhattan_distance(sensor, (x, y)) <= distance:
                    valid = False
                    break

            if valid:
                return x, y

    return None


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, target_y=10 if is_test else 2000000)
    return len(result)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data_2(data, max_value=20 if is_test else 4000000)
    return 4000000 * result[0] + result[1]


if __name__ == '__main__':
    is_test = False
    # print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
