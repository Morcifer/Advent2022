from typing import List, Optional, Tuple, Dict

from src.utilities import load_data

DAY = 10


def parser(s: List[str]) -> Optional[int]:
    if s[0] == "noop":
        return None

    return int(s[1])


interesting_cycles = list(range(20, 221, 40))


def process_data(data: List[Optional[int]]) -> Dict[int, int]:
    result = {}

    cycle = 1
    value = 1

    for datum in data:
        previous_cycle = cycle
        previous_value = value

        if datum is None:
            # Do nothing
            cycle += 1
        else:
            cycle += 2
            value += datum

        for c in range(previous_cycle, cycle):
            result[c] = previous_value

    for c in range(cycle, interesting_cycles[-1]):
        # print(f"End of cycle {c} has value {value}")
        if c in interesting_cycles:
            result[c] = value

    return result


def translate_pixel_instructions(data: Dict[int, int]) -> None:
    for start, end in zip(range(1, 202, 40), range(40, 241, 40)):
        row = []
        for printed_pixel_spot in range(0, 40):
            cycle = start + printed_pixel_spot
            location_of_pixie = data[cycle]
            if abs(printed_pixel_spot - location_of_pixie) <= 1:
                row.append("#")
            else:
                row.append(".")

        print("".join(row))

    return


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    return sum(c * v for c, v in result.items() if c in interesting_cycles)


def part_2(is_test: bool) -> None:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    translate_pixel_instructions(result)
    return None


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
