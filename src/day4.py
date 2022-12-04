from typing import List, Optional, Tuple

from src.utilities import load_data


DAY = 4


def parser(s: List[str]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    elf1, elf2 = s[0].split(",")
    elf1 = elf1.split("-")
    elf2 = elf2.split("-")
    return (int(elf1[0]), int(elf1[1])), (int(elf2[0]), int(elf2[1]))


def process_data(data: List[Tuple[str, str]]) -> Tuple[List[bool], List[bool]]:
    contained, overlaps = [], []

    for (elf1_s1, elf1_s2), (elf2_s1, elf2_s2) in data:
        elf1_in_elf2 = elf2_s1 <= elf1_s1 and elf1_s2 <= elf2_s2
        elf2_in_elf1 = elf1_s1 <= elf2_s1 and elf2_s2 <= elf1_s2

        if elf1_in_elf2 or elf2_in_elf1:
            contained.append(True)

        if elf2_s1 <= elf1_s2 and elf1_s1 <= elf2_s2:
            overlaps.append(True)

    return contained, overlaps


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return len(process_data(data)[0])


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return len(process_data(data)[1])


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
