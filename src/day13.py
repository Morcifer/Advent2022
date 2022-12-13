import itertools
from functools import partial, cmp_to_key
from typing import List, Optional, Tuple, Dict

from src.utilities import load_data

DAY = 13


def parser(s: List[List[str]]) -> Tuple[str, str]:
    return eval(s[0][0]), eval(s[1][0])


def process_data(data: List[Tuple]) -> List[int]:
    result = []

    for index, (packet_left, packet_right) in enumerate(data):
        comparison = compare_values(packet_left, packet_right)
        if comparison == -1:
            result.append(index + 1)
        elif comparison == 0:
            raise ValueError("You have a bug!")

    return result


buffer_1 = [[2]]
buffer_2 = [[6]]


def flatten(sequence):
    return list(itertools.chain(*sequence))


def order_data(data: List[Tuple]) -> List:
    everything = [buffer_1, buffer_2] + flatten([left, right] for left, right in data)
    everything = sorted(everything, key=cmp_to_key(compare_values))

    return everything


def compare_values(left_input, right_input) -> int:
    left_input = left_input[:]
    right_input = right_input[:]

    while len(left_input) > 0 and len(right_input) > 0:
        left = left_input.pop(0)
        right = right_input.pop(0)

        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return -1

            if left > right:
                return 1

            continue

        if isinstance(left, list) and isinstance(right, list):
            comparison = compare_values(left, right)
            if comparison != 0:
                return comparison

            continue

        if isinstance(left, int) and isinstance(right, list):
            new_left = [left]
            comparison = compare_values(new_left, right)
            if comparison != 0:
                return comparison

            continue

        if isinstance(left, list) and isinstance(right, int):
            new_right = [right]
            comparison = compare_values(left, new_right)
            if comparison != 0:
                return comparison

            continue

    if len(left_input) == 0 and len(right_input) > 0:
        return -1

    if len(right_input) == 0 and len(left_input) > 0:
        return 1

    return 0


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test, cluster_at_empty_line=True)
    result = process_data(data)
    return sum(result)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test, cluster_at_empty_line=True)
    result = order_data(data)
    for i, packet in enumerate(result):
        if packet == buffer_1:
            first_spot = i+1
        if packet == buffer_2:
            last_spot = i +1

    return first_spot * last_spot


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
