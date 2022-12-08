from typing import List, Optional, Tuple, Dict

from src.utilities import load_data

DAY = 8


def parser(s: List[str]) -> List[int]:
    return [int(c) for c in s[0]]


def process_data(data: List[List[int]]) -> List[Tuple[int, int]]:
    visible_spots = []
    size = len(data)

    for i in range(size):
        for j in range(size):
            spot = (i, j)
            this_tree_height = data[i][j]

            if i in [0, size - 1] or j in [0, size - 1]:
                visible_spots.append(spot)
                continue

            max_of_row_before = max(data[x][j] for x in range(size) if x < i)
            max_of_row_after = max(data[x][j] for x in range(size) if x > i)
            max_of_column_before = max(data[i][x] for x in range(size) if x < j)
            max_of_column_after = max(data[i][x] for x in range(size) if x > j)

            if (max_of_row_before < this_tree_height
                    or max_of_row_after < this_tree_height
                    or max_of_column_before < this_tree_height
                    or max_of_column_after < this_tree_height
            ):
                visible_spots.append(spot)
                continue

            # print(f"{spot} is NOT visible, has height {this_tree_height}")

    return visible_spots


def process_data_2(data: List[List[int]]) -> int:
    best_score = 0
    size = len(data)

    for i in range(size):
        for j in range(size):
            spot = (i, j)
            this_tree_height = data[i][j]

            if i in [0, size - 1] or j in [0, size - 1]:
                continue

            for score_row_before, x in enumerate(range(i-1, -1, -1)):
                if data[x][j] >= this_tree_height:
                    break

            for score_row_after, x in enumerate(range(i+1, len(data))):
                if data[x][j] >= this_tree_height:
                    break

            for score_column_before, x in enumerate(range(j-1, -1, -1)):
                if data[i][x] >= this_tree_height:
                    break

            for score_column_after, x in enumerate(range(j+1, len(data))):
                if data[i][x] >= this_tree_height:
                    break

            score_row_before += 1
            score_row_after += 1
            score_column_before += 1
            score_column_after += 1

            this_score = score_row_before * score_row_after * score_column_before * score_column_after
            best_score = max(best_score, this_score)
            # print(f"Spot {spot} with height {this_tree_height} has score {this_score}")

    return best_score


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    return len(result)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data_2(data)
    return result


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
