import itertools
import math
from collections import Counter
from copy import deepcopy
from functools import partial, cmp_to_key
from typing import List, Optional, Tuple, Dict, Set

from src.utilities import load_data

DAY = 25


def flatten(sequence):
    return list(itertools.chain(*sequence))


def parser(s: List[str]) -> str:
    return s[0]


# Instead of using digits four through zero, the digits are 2, 1, 0, minus (written -),
# and double-minus (written =). Minus is worth -1, and double-minus is worth -2.
proper_numerals = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}

snafu_numerals = {value: key for key, value in proper_numerals.items()}


def snafu_to_proper(input: str) -> int:
    result = 0

    for character in input:
        result *= 5
        result += proper_numerals[character]

    return result


def proper_to_snafu(input: int) -> str:
    result = []
    value = input

    while value != 0:
        nearest_5_below = 5 * int(math.floor(value / 5.0))
        nearest_5_above = 5 * int(math.ceil(value / 5.0))

        if value - nearest_5_below in [0, 1, 2]:
            result.insert(0, snafu_numerals[value - nearest_5_below])
            value = nearest_5_below
        else:
            result.insert(0, snafu_numerals[value - nearest_5_above])
            value = nearest_5_above

        value = int(value / 5)

        print("".join(result))

    return "".join(result)


def process_data(data: List[str]) -> List[int]:
    return [snafu_to_proper(datum) for datum in data]


def part_1(is_test: bool) -> str:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    return proper_to_snafu(sum(result))


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
