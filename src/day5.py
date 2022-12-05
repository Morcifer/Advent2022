from typing import List, Optional, Tuple

from src.utilities import load_data, load_data_un_parsed

DAY = 5


class CrateStacks:
    def __init__(self, data):
        number_of_stack = int(data[-1].split()[-1])
        stacks = []

        for stack in range(0, number_of_stack):
            stacks.append([])
            for height in range(1, len(data)):
                row = data[len(data) - height - 1]
                if stack * 4 + 1 <= len(row):
                    crate = row[stack * 4 + 1]
                    if crate.strip() != "":
                        stacks[-1].append(crate)

        self.stacks = stacks

    def apply_move(self, how_many, from_where, to_where):
        for _ in range(how_many):
            crate = self.stacks[from_where - 1].pop()
            self.stacks[to_where - 1].append(crate)

    def apply_super_move(self, how_many, from_where, to_where):
        removed = []
        for _ in range(how_many):
            crate = self.stacks[from_where - 1].pop()
            removed.insert(0, crate)

        self.stacks[to_where - 1].extend(removed)


def parser(s: List[str]) -> Tuple[int, int, int]:
    # move 1 from 1 to 2
    return int(s[1]),  int(s[3]), int(s[5])


def process_data(crate_stacks: CrateStacks, data: List[Tuple[int, int, int]], super_mover=False) -> List[str]:
    for datum in data:
        if super_mover:
            crate_stacks.apply_super_move(datum[0], datum[1], datum[2])
        else:
            crate_stacks.apply_move(datum[0], datum[1], datum[2])

    return [stack[-1] for stack in crate_stacks.stacks]


def part_1(is_test: bool) -> str:
    data0 = load_data_un_parsed(DAY, "data", is_test=is_test, suffix="0")
    crate_stacks = CrateStacks(data0)
    data = load_data(DAY, parser, "data", is_test=is_test)
    tops = process_data(crate_stacks, data)
    return "".join(tops)


def part_2(is_test: bool) -> str:
    data0 = load_data_un_parsed(DAY, "data", is_test=is_test, suffix="0")
    crate_stacks = CrateStacks(data0)
    data = load_data(DAY, parser, "data", is_test=is_test)
    tops = process_data(crate_stacks, data, super_mover=True)
    return "".join(tops)


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
