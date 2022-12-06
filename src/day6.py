from typing import List, Optional, Tuple

from src.utilities import load_data

DAY = 6


def parser(s: List[str]) -> str:
    return s[0]


def process_data(datum: str, distinct) -> int:
    for i in range(distinct, len(datum)):
        substring = datum[i - distinct: i]
        if len(set(substring)) == len(substring):
            return i

    return -1


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)[0]
    result = process_data(data, distinct=4)
    return result


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)[0]
    result = process_data(data, distinct=14)
    return result


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
