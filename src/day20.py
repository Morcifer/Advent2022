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


def process_data(data: List[int]) -> List[int]:
    # We cannot assume the list is unique. We have to keep track of indices.
    original_numbers = data[:]
    original_indices = list(range(len(data)))
    current_indices = list(range(len(data)))

    for index in original_indices:
        # print(data)

        number = original_numbers[index]
        old_index = current_indices[index]

        if data[old_index] != number:
            print("There's an offset somewhere!")

        new_index = old_index + number

        if number < 0:
            new_index = (new_index % len(data)) - 1

        if new_index == -1:
            # Coundary condition.
            new_index = len(data)

        if new_index > len(data):
            new_index = (new_index % len(data)) + 1

        print(f"Moving {number} (old index {index} out of {len(data)}) from {old_index} to {new_index}")

        if new_index == old_index:
            continue

        for i in range(len(current_indices)):
            if current_indices[i] > old_index:
                current_indices[i] -= 1

        for i in range(len(current_indices)):
            if current_indices[i] > new_index - 1:
                current_indices[i] += 1

        current_indices[index] = new_index

        del data[old_index]
        data.insert(new_index, number)

    return data


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)

    print(data)

    # Find the 0:
    spot = next(i for i, n in enumerate(result) if n == 0)

    # 1000th, 2000th, and 3000th
    n1 = result[(spot + 1000) % len(result)]
    n2 = result[(spot + 2000) % len(result)]
    n3 = result[(spot + 3000) % len(result)]

    return n1 + n2 + n3


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    return result


if __name__ == '__main__':
    is_test = True
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    # print(f"Day {DAY} result 2: {part_2(is_test)}")
