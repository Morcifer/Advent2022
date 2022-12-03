from typing import List, Optional, Tuple

from src.utilities import load_data


DAY = 3


def parser(s: List[str]) -> Tuple[str, str]:
    half = int(len(s[0]) / 2)
    return s[0][:half], s[0][half:]


def get_priority(s):
    if s.islower():
        # Lowercase item types a through z have priorities 1 through 26.
        return ord(s) - 96
    else:
        # Uppercase item types A through Z have priorities 27 through 52.
        return ord(s) - 38


def process_data_1(data: List[Tuple[str, str]]) -> List[int]:
    results = []

    for compartment_1, compartment_2 in data:
        in_both = list(set(compartment_1).intersection(set(compartment_2)))[0]
        priority = get_priority(in_both)
        results.append(priority)

    return results


def process_data_2(data: List[Tuple[str, str]]) -> List[int]:
    results = []

    for first_elf_index in range(0, len(data), 3):
        elf_1 = "".join(data[first_elf_index])
        elf_2 = "".join(data[first_elf_index + 1])
        elf_3 = "".join(data[first_elf_index + 2])

        badge = list(set(elf_1).intersection(set(elf_2)).intersection(set(elf_3)))[0]
        priority = get_priority(badge)
        results.append(priority)

    return results


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return sum(process_data_1(data))


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return sum(process_data_2(data))


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
