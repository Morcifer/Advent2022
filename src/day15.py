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


def process_data_2(data: List[Tuple[Tuple[int, int], Tuple[int, int]]], max_value: int) -> List[Tuple[int, int]]:
    ruled_out_ranges_per_y = {}

    for i, (sensor, beacon) in enumerate(data):
        print(f"I'm at sensor {i + 1} out of {len(data)}, which is at {sensor} with beacon at {beacon}")
        distance = manhattan_distance(sensor, beacon)
        min_y = max(0, sensor[1] - distance)
        max_y = min(max_value, sensor[1] + distance)

        for y in range(min_y, max_y + 1):
            y_distance = abs(sensor[1] - y)
            remaining_distance = abs(distance - y_distance)
            min_x = max(0, sensor[0] - remaining_distance)
            max_x = min(max_value, sensor[0] + remaining_distance)

            if y in ruled_out_ranges_per_y:
                old_ranges = ruled_out_ranges_per_y[y]
                for range_min, range_max in old_ranges:
                    # If overlap - is bigger now!
                    if range_min <= max_x and min_x <= range_max or range_max + 1 == min_x or max_x + 1 == range_min:
                        min_x = min(min_x, range_min)
                        max_x = max(max_x, range_max)

                new_ranges = [
                    (range_min, range_max)
                    for (range_min, range_max) in old_ranges
                    if not (min_x <= range_min <= range_max <= max_x)
                ]  # Get rid of anything that's already in it.

                new_ranges.append((min_x, max_x))
                ruled_out_ranges_per_y[y] = new_ranges
            else:
                ruled_out_ranges_per_y[y] = [(min_x, max_x)]

    answers = []

    for y, value in ruled_out_ranges_per_y.items():
        if len(value) != 1:
            lower_range, upper_range = value

            if lower_range[0] > upper_range[0]:  # Swap please!
                lower_range, upper_range = upper_range, lower_range

            if lower_range[0] != 0 and upper_range[1] != max_value:
                print(f"Something is wrong, for y {y} I have ranges {value}")

            x = lower_range[1] + 1
            print(f"I think the answer is {x}, {y}, which is to say {4000000 * x + y}")
            answers.append((x, y))

    return answers


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, target_y=10 if is_test else 2000000)
    return len(result)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data_2(data, max_value=20 if is_test else 4000000)
    result = result[0]
    return 4000000 * result[0] + result[1]  # Not 16000006855041, yes 11645454855041!


if __name__ == '__main__':
    is_test = False
    # print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
