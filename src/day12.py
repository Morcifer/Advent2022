from typing import List, Optional, Tuple, Dict

from src.utilities import load_data

DAY = 12


def parser(s: List[str]) -> str:
    return s[0]


def process_data(data: List[str]) -> List[str]:
    # First, find the starting point and ending point
    for i, row in enumerate(data):
        for j, character in enumerate(row):
            if character == "S":
                start = (i, j)
            if character == "E":
                end = (i, j)

    # Then, DPS, saving the route as well.
    to_explore = [(start, [start])]
    explored = {}

    while len(to_explore) != 0:
        here, route_to_here = to_explore.pop(0)
        i, j = here
        this_altitude = ord(data[i][j]) if data[i][j] != "S" else ord("a") - 1

        if here in explored:
            continue

        if here == end:
            return [data[i][j] for i, j in route_to_here]

        explored[here] = route_to_here

        for neighbour in [(i, j+1), (i, j-1), (i+1, j), (i-1, j)]:
            try:
                neighbour_letter = data[neighbour[0]][neighbour[1]]
            except IndexError:
                continue

            neighbour_altitude = ord(neighbour_letter) if neighbour_letter != "E" else ord("z") + 1

            if neighbour_altitude > this_altitude + 1:
                continue

            to_explore.append((neighbour, route_to_here + [neighbour]))

    return []


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    print("".join(result))
    return len(result) - 1


def part_2(is_test: bool) -> int:
#     data = load_data(DAY, parser, "data", is_test=is_test)
#     result = process_data(data)
#     return sum(c * v for c, v in result.items() if c in interesting_cycles)
    pass


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
