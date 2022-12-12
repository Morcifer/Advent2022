from typing import List, Optional, Tuple, Dict

from src.utilities import load_data

DAY = 12


def parser(s: List[str]) -> str:
    return s[0]


def process_data(data: List[str], valid_starting_letters: List[str]) -> List[List[str]]:
    # First, find the starting points and ending points
    all_valid_starts = []
    for valid_starting_letter in valid_starting_letters:
        for i, row in enumerate(data):
            for j, character in enumerate(row):
                if character == valid_starting_letter:
                    all_valid_starts.append((i, j))
                if character == "E":
                    end = (i, j)

    return [find_shortest_path(data, start, end) for start in all_valid_starts]

def find_shortest_path(data: List[str], start, end) -> List[List[str]]:
    # Then, BFS, saving the route as well.
    to_explore = [(start, [start])]
    explored = {}

    while len(to_explore) != 0:
        here, route_to_here = to_explore.pop()
        i, j = here

        if here in explored:
            continue

        if here == end:
            route = [data[i][j] for i, j in route_to_here]
            # print("".join(route))
            return route

        explored[here] = route_to_here
        this_altitude = ord("a") if data[i][j] == "S" else ord(data[i][j])

        for neighbour in [(i, j+1), (i, j-1), (i+1, j), (i-1, j)]:
            if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= len(data) or neighbour[1] >= len(data[0]):
                continue

            neighbour_letter = data[neighbour[0]][neighbour[1]]

            neighbour_altitude = ord("z") if neighbour_letter == "E" else ord(neighbour_letter)

            if neighbour_altitude > this_altitude + 1:
                continue

            to_explore.insert(0, (neighbour, route_to_here + [neighbour]))

    return []


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, valid_starting_letters=["S"])
    return len(result[0]) - 1


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    results = process_data(data, valid_starting_letters=["S", "a"])
    return min(len(result) - 1 for result in results if len(result) != 0)


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
