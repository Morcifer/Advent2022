import itertools
import math
from copy import deepcopy
from functools import partial, cmp_to_key
from typing import List, Optional, Tuple, Dict, Set

from src.utilities import load_data

DAY = 20


def flatten(sequence):
    return list(itertools.chain(*sequence))


def parser(s: List[str]) -> int:
    return int(s[0])


def process_data(data: List[int], key: int, times_to_mix: int) -> int:
    data = [n * key for n in data]

    # We cannot assume the list is unique. We have to keep track of everything.
    indexed_numbers = [(i, n) for i, n in enumerate(data)]

    for i in range(times_to_mix):
        for index in range(len(data)):
            current_index, original_index, number = next(
                (current_index, original_index, number)
                for current_index, (original_index, number) in enumerate(indexed_numbers)
                if original_index == index
            )

            new_index = (current_index + number) % (len(data) - 1)  # Because we remove _before_ shifting. :/

            del indexed_numbers[current_index]
            indexed_numbers.insert(new_index, (original_index, number))

    numbers = [number for _, number in indexed_numbers]

    # Find the 0:
    spot = next(i for i, n in enumerate(numbers) if n == 0)

    # 1000th, 2000th, and 3000th
    n1 = numbers[(spot + 1000) % len(numbers)]
    n2 = numbers[(spot + 2000) % len(numbers)]
    n3 = numbers[(spot + 3000) % len(numbers)]

    return n1 + n2 + n3


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, key=1, times_to_mix=1)
    return result


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, key=811589153, times_to_mix=10)
    return result


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
