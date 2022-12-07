from typing import List, Optional, Tuple, Dict

from src.utilities import load_data

DAY = 7


def parser(s: List[str]) -> List[str]:
    return s


def process_data(data: List[str]) -> Dict[str, int]:
    all_folders = {"/": 0}
    all_files = {}

    current_path = []
    disc = {"/": {}}
    current_folder = disc

    for i, datum in enumerate(data):
        if datum[0] == "$":
            if datum[1] == "ls":
                continue

            # Switching somewhere new
            if datum[1] == "cd":
                if datum[2] == "..":
                    current_path = current_path[:-1]

                    current_folder = disc
                    for go_to in current_path:
                        current_folder = current_folder[go_to]
                else:
                    current_path = current_path + [datum[2]]
                    try:
                        current_folder = current_folder[datum[2]]
                    except:
                        print("meh")
        else:
            # This is the results of the ls command
            if datum[0] == "dir":
                current_folder[datum[1]] = {}
                all_folders["".join(current_path) + datum[1]] = 0
                continue

            current_folder[datum[1]] = datum[0]
            all_files[datum[1]] = datum[0]

            for i in range(0, len(current_path)):
                whole_path = "".join(current_path[:i+1])
                all_folders[whole_path] += int(datum[0])

    return all_folders


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    return sum([size for folder, size in result.items() if folder != "/" and size < 100000])


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    size_remaining = 70000000 - result["/"]
    sizes = list(result.values())
    sizes.sort()
    for size in sizes:
        if size_remaining + size > 30000000:
            return size

    return -1


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
