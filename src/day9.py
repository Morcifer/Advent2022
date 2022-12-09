from typing import List, Optional, Tuple, Dict

from src.utilities import load_data

DAY = 9


def parser(s: List[str]) -> Tuple[str, int]:
    return s[0], int(s[1])


def process_data(data: List[Tuple[str, int]], tails: int) -> List[Tuple[int, int]]:
    knots = [(0, 0) for _ in range(tails + 1)]
    visited_tail_spots = [knots[-1]]

    for i, (direction, amount) in enumerate(data):
        for _ in range(amount):
            head_x, head_y = knots[0]

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

            knots[0] = head_x, head_y

            for knot_index in range(1, tails + 1):
                head_x, head_y = knots[knot_index - 1]
                tail_x, tail_y = knots[knot_index]

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

                knots[knot_index] = tail_x, tail_y

            visited_tail_spots.append(knots[-1])

    return visited_tail_spots


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, tails=1)
    return len(set(result))


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, tails=9)
    return len(set(result))


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
