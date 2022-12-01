from typing import List, Optional

from src.utilities import load_data


def parser(s: List[str]) -> Optional[int]:
    return None if s[0] == "" else int(s[0])


def divide_rations(data: List[int]) -> List[int]:
    rations_per_elf = [[]]
    for datum in data:
        if datum is None:
            rations_per_elf.append([])
        else:
            rations_per_elf[-1].append(datum)

    return [sum(rations) for rations in rations_per_elf]


def part_1() -> int:
    data = load_data(1, parser, "data", is_test=False)
    return max(divide_rations(data))


def part_2() -> int:
    data = load_data(1, parser, "data", is_test=False)
    total_rations_per_elf = divide_rations(data)
    total_rations_per_elf = sorted(total_rations_per_elf, reverse=True)

    return sum(total_rations_per_elf[:3])


if __name__ == '__main__':
    print(f"Result 1: {part_1()}")
    print(f"Result 2: {part_2()}")
