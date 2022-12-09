from typing import List, Optional, Tuple, Dict

from src.utilities import load_data

DAY = 9


def parser(s: List[str]) -> Tuple[str, int]:
    return s[0], int(s[1])


def process_data(data: List[Tuple[str, int]]) -> List[Tuple[int, int]]:
    head_x, head_y = 0, 0
    tail_x, tail_y = 0, 0
    visited_tail_spots = [(tail_x, tail_y)]

    for i, (direction, amount) in enumerate(data):
        for _ in range(amount):
            if direction == "U":
                head_y += 1
            elif direction == "D":
                head_y -= 1
            elif direction == "R":
                head_x += 1
            elif direction == "L":
                head_x -= 1
            else:
                raise ValueError("?")

            if abs(head_x - tail_x) <= 1 and abs(head_y - tail_y) <= 1:
                continue

            if head_x > tail_x:
                tail_x += 1
            elif head_x < tail_x:
                tail_x -= 1

            if head_y > tail_y:
                tail_y += 1
            elif head_y < tail_y:
                tail_y -= 1

            visited_tail_spots.append((tail_x, tail_y))

    return visited_tail_spots



def process_data_2(data: List[Tuple[str, int]]) -> List[Tuple[int, int]]:
    head_x, head_y = 0, 0
    tail_xs = [0 for _ in range(9)]
    tail_ys = [0 for _ in range(9)]

    visited_tail_spots = [(tail_xs[-1], tail_ys[-1])]

    for i, (direction, amount) in enumerate(data):
        for _ in range(amount):
            if direction == "U":
                head_y += 1
            elif direction == "D":
                head_y -= 1
            elif direction == "R":
                head_x += 1
            elif direction == "L":
                head_x -= 1
            else:
                raise ValueError("?")

            for tail_index in range(9):
                relevant_head_x = head_x if tail_index == 0 else tail_xs[tail_index - 1]
                relevant_head_y = head_y if tail_index == 0 else tail_ys[tail_index - 1]

                tail_x = tail_xs[tail_index]
                tail_y = tail_ys[tail_index]

                if abs(relevant_head_x - tail_x) <= 1 and abs(relevant_head_y - tail_y) <= 1:
                    continue

                if relevant_head_x > tail_x:
                    tail_x += 1
                elif relevant_head_x < tail_x:
                    tail_x -= 1

                if relevant_head_y > tail_y:
                    tail_y += 1
                elif relevant_head_y < tail_y:
                    tail_y -= 1

                tail_xs[tail_index] = tail_x
                tail_ys[tail_index] = tail_y

            visited_tail_spots.append((tail_xs[-1], tail_ys[-1]))

    return visited_tail_spots


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    return len(set(result))


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data_2(data)
    return len(set(result))


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
