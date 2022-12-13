from typing import List, Optional, Tuple, Dict

from src.utilities import load_data

DAY = 13


def parser(s: List[List[str]]) -> Tuple[str, str]:
    return eval(s[0][0]), eval(s[1][0])


def process_data(data: List[Tuple]) -> List[int]:
    result = []

    for index, (packet_left, packet_right) in enumerate(data):
        comparison = compare_values(packet_left, packet_right)
        if comparison is True:
            print(packet_left, packet_right, "right order")
            result.append(index + 1)
        else:
            print(packet_left, packet_right, "wrong order")

    return result


def compare_values(left_input, right_input) -> bool:
    left_input = left_input[:]
    right_input = right_input[:]

    while len(left_input) > 0 and len(right_input) > 0:
        left = left_input.pop(0)
        right = right_input.pop(0)

        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return True

            if right < left:
                return False

        if isinstance(left, list) and isinstance(right, list):
            comparison = compare_values(left, right)
            if comparison is not None:
                return comparison

        if isinstance(left, int) and isinstance(right, list):
            new_left = [left]
            comparison = compare_values(new_left, right)
            if comparison is not None:
                return comparison

        if isinstance(left, list) and isinstance(right, int):
            new_right = [right]
            comparison = compare_values(left, new_right)
            if comparison is not None:
                return comparison

    if len(left_input) == 0:
        return True

    if len(right_input) == 0:
        return False

    return None


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test, cluster_at_empty_line=True)
    result = process_data(data)
    return sum(result)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test, cluster_at_empty_line=True)
    result = process_data(data)
    return sum(result)


if __name__ == '__main__':
    is_test = True
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    # print(f"Day {DAY} result 2: {part_2(is_test)}")
