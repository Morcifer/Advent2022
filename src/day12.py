from typing import List, Optional, Tuple, Dict

from src.utilities import load_data

DAY = 12


def parser(s: List[str]) -> str:
    return s[0]


def get_altitude(letter) -> int:
    if letter == "S":
        return ord("a")

    if letter == "E":
        return ord("z")

    return ord(letter)


def process_data(data: List[str], part_1: bool) -> List[str]:
    # First, find the starting point
    start_letter = "S" if part_1 else "E"

    for i, row in enumerate(data):
        for j, character in enumerate(row):
            if character == start_letter:
                start = (i, j)

    # Then, BFS, saving the route as well.
    to_explore = [(start, [start])]
    explored = {}

    while len(to_explore) != 0:
        here, route_to_here = to_explore.pop()
        i, j = here

        if here in explored:
            continue

        this_letter = data[i][j]

        are_we_there_yet = (
            this_letter == "E" if part_1
            else this_letter == "S" or this_letter == "a"
        )

        if are_we_there_yet:
            route = [data[i][j] for i, j in route_to_here]
            return route

        explored[here] = route_to_here
        this_altitude = get_altitude(this_letter)

        for neighbour in [(i, j+1), (i, j-1), (i+1, j), (i-1, j)]:
            if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= len(data) or neighbour[1] >= len(data[0]):
                continue

            neighbour_letter = data[neighbour[0]][neighbour[1]]
            neighbour_altitude = get_altitude(neighbour_letter)

            if part_1:
                # Can only go one up, but any amount down
                if neighbour_altitude > this_altitude + 1:
                    continue
            else:
                # Can only go one down, but any amount up
                if neighbour_altitude < this_altitude - 1:
                    continue

            to_explore.insert(0, (neighbour, route_to_here + [neighbour]))

    return []


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, part_1=True)
    return len(result) - 1


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, part_1=False)
    return len(result) - 1


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
