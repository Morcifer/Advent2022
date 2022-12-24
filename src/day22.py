import itertools
import math
from copy import deepcopy
from enum import Enum
from functools import partial, cmp_to_key
from typing import List, Optional, Tuple, Dict, Set, Union

from src.utilities import load_data

DAY = 22


def flatten(sequence):
    return list(itertools.chain(*sequence))


def parser(s: List[str]) -> str:
    return "".join(s)


def parse_instructions(s: str) -> List[str]:
    result = []

    start = 0

    while start < len(s):
        end = start
        for end in range(start, len(s)):
            if s[end] == "L" or s[end] == "R":
                break

        if end == start == len(s) - 1:
            end += 1

        result.append(int(s[start:end]))

        if end < len(s):
            result.append(s[end])

        start = end + 1

    return result


test_path = "10R5L5R10L4R5L5"
real_path = "12R25R28R21L15R49L21R10R27R28L47L18R43L1R8L34R4R34L48L42L19R32R30R34L11L49L6R49L5R45R11L6R47L27L12R46L40R46L33L14R18R41R12L25L35L29L16R41L14R32L29L49L24L35R39L8R34L20L19L14R44R12L35R10L35L11L46R35R14R21L10R10L31L2L47L10L40R43L8L8L38L6L49L27L14L21L49L45L29L7L28L41L10L4R28R7R48L5R6L25L47R40R30R34L39R35L46L39R24L45L26R44R13L36L15R35R7R42R34L3L28R42R2R32R42R22R23R9R34R32R34L10L22R10L31L17L23L45R14R2R34R10R45L28R30L25R20R41L1L29R31R11R37R18L50L50R12L33L6R49L50R12R2L3R42R9L7L44R30L26L1R37R22R18R50R17L23L5R8R48L30R33L2R46L49L1L18R37R50L10R8L7R8R37R30R14R40L36L15L41L46R39R8L4L34R11L25R37L23R18R47L23R32L26R49R16R30R12R39L7L43R38R45L50L35R46L24L41R3R18R5L12L39R41L46R31L12L48L7R21L22R5L27R42L26R20R40R9R8R22R6R41R40L33L24L30L45L29R18R20R5L31L4L40L49R37R9L17R4R34R47L18L48L4L8R4L5L40L7R47L29R49R50R50L22R23R21L50L17L28L41L38R6R36L12L9R9R40L16L4R44L7L37R14L10R16R38R44L35R19R47R18R29L31L40L47R35L42L7L34L49R10L29L14R12R24R13L29L12R45R8R50R39R34L50L10R44L32L31L24L30R47R41R2L7R3R31R38R33R35R46L22R12R47L20L36R49R27L3R25L2L12R13L28L17L29L44L18L35L18R6R22R24L38L31R23R26L39R40R13L37L24R1R14L20L14R43R14R45R36R22R47R22L18R17L28L45R22L20L19R37R20L43L43L14L8R16R6L13R6L23R16L1L45R9R36R17L45L30R43L31L38L4L28L27R12L7R27R50R49L4L30L21R27R46L44R17L15L5L4L29R31R19L13R48L36L8L17R23R1R40L33R50R12L36L19L6L45L17L14R12R3L36L35L19R46R21L8L33L11L34L25L2R32R10R30R15R46R37R24R39R7R39R43L29R39L34R29R19R49R41L38R11L43R17L35L45R41L22R48R25R8R45R39R13R8L36R2R5R50L40L12L23R42L2R41R14R19R28L25L49R39R9R13L43L20L28L46R19R36R46R12L9R7R30R30R9R43R26R36L11L34R41L42L19R2L18R9R20R11L11L2L10L24R25R32L44R14R4R24R10R24L5R4L13R35R35R22L18L24R46L32L47L37R21R49R6R12L16L31L39L26L48L8L26R27R16L48L30R36L24L48R36L1L1R16L38R1R26L11L29R20L50R22R44R4L18R37L6L19L44R20R14R37R3L39R12L23L46L19L45R35L12L7L28R46L18R25R38R10L22R18R34L25R4L15L2L9L35L24R6R27R22R32L22L49R22L39L27L38R38R12R28L27R2R14R10R30L25R4L15L40R34R42R38R9R12L14L15R34R6R9R41R11R47R23R25R37R31L21R37R4R15L20R37R33L13R23R38R23R42R37L17L34R21R36R21R39R14L35R3R9L33R45R37R32R18R26L27R39R50R37R34L41R48L43L37L23L42L8L2R25R16L6R11L2L5L41L25L6L41L46L1R25L31R26L25L26R18L46R1R14R15R29R29R34R19R28L50R35R10R10L41L4R15R36L7L36L7R36L40R16L33L16L23R45R32R43L10L42R11L7R18L17R14R25L47L38R46L28R21L43R29R44L20R45L29R3L1L38R32R42L15L46L22R22L26R42R12R38R3L5R4R17L1L34R33R9L39R32R22R19R43L50L32R15R21L14L35L7L31R9R28R50R25R13L22L32R46L37L16L39L19L31R17R47R29R21L24L49L9R48L13R26L43L35L5L4R45L38R29R1L40L5R50R1L49R46L40L30R41R4L11R40R35L14L15R21R17L22L18R37R49R3L21R22L36L14R43R9L24L39R11L39L6L49R46R39L15L37L44R25R48R46L38R7L12R18R12R14R44R37R23R42R37L50L9L27R36L18R14R3L5R38R44L35R36L12L41L15R6L39L40R5L2R18R36R38L26R38L22R21R5R1L11L29R2L34L41L29R32R25L37R3L34L18L14L33L17R48L47L12R26R35L22L16R20R24R22R38R18R13R37R31R22R42R37R34R45R21L27L14L29L16R15L1L9R49L14R40R33R3L30L32L32R16L22R44L43R22R39L9L50L16R9R18L12R27R10R10R27L27R40R10L46R32L44L9L48R28R29R23L45L26L37L38L29R27R35R19L46R44R13R2L27R46R48L42R27R43R27R23R20R23L40L36R29R2L22R15R14R33L45R14R32R1R43L20R20L15L44L22L4L24R22L23R29R34L28L15R48L28L26L26R16L40L11L27R29L27R28L5L6R30L8R35R44L29L48L11L29R2L21R10R29L45L31L16L12R16R14R25R49R17L41R31R2R45L11R10R41R34R12R39R9R6R9L29R19R43R3R28L29L9R27R3R9L40R36R47L9L11L44L31R16L50R32L7L49R26R33R48L49L34R43R1L14L1R19R4L15R11R34L13R36L2R32L33R19L16L22R6R9L23R25L9L35L46R15L26L7R40L35R45L49L47R27R3R39R17R46L47R46L23L36R50L16R45R1L4R39R32L33R18L35R41R44L20R39L37L14L33L23L23R22L13L14R43R31R2L24L26R49L38R38L25L28L29R50L16L31L20R38R42L7R20L42L12R39L35L16L11L22L28L7L16L50L3L42L38R23R37R30R48L16R36R49R27R19R39R14L35L12R14R14R1R19L50R28R26L33L28R35L25R24R48R27L44L34L46R49L6R24R19L7L39R6L28L43L14L40R10L27R12R45L4L7R35L38R45L50L8L33L22R28R27R30R30R3L23R28R9L39L7L21L40L18R43R50R31R33L26L34R25L1L43L21L50R14L20R2R4L13L24R38L10L43R34L30R21L20R12R12R16R23L21L46R39R32R7R20R19R37L48L12L40R14L33R17L32R24L28L45R17L13R6L9R28L46L35R49R9L4L43L38L22R15L48L11R38L24R5R2R49R43R12L18R21R36L24R3L30R10L30R47R48R46R31L9L45R1L48R21R14R5R2L46L10L27L22R15R34R42L26R43R17L36R13R14R44L24L34L9L29L38R16L40R39R29L15R42L18L3R40L30R40L2L29R38L43R32R34L3L4R32L28L49L4R42R37L16L46R27L15R5R28L36R24L27R22L37L23R21R1R24L13R3L43R8L30R16R36L46L21L46L27L30L2R4L8R34R1R2L9R8R18L50L13L26L37L18L43L42R39R33R27R24L49R24L9L50L45L32R33R10L12R28R15R14L44L45L20R41L5R30L33R15L22L41R46R20L36R23R2L29L45L26R44R25R21R6R45R3L41L49L48L43R43R49R6R17L48R7R21L36L49L15R43R36L28R40L9R23L19L10R4R14L20L7L21L46R12R28R32L39R4R19L25R7L34R38R22L7L5L22R44R20R10R24L45R45L11L48L23L8L34R27L17R27L47L2L9L49R1R32R40L39R1R18R50L29L19R32R38L26L17R36R40R31L29L29R44L25R37R3R13L43L18R33R5R9R31L23L17R1R10R37R12L21L6R47R38R44R3L11R13L41L24R39L14L7R21L25R39R45R44L34L1L41R7L44L8L19R30R7L7R44L9L8L46L19R31R44L19R41L21R4L34L12L44R4R20R19R34L7L8L9R34R34R4L12R2R41L50R11L6R14R40R35L43L47L7R40R29L11L45R32R10R1R25L14R19L38L20L7L29R19L30R3R23L34R40L34R2R40L46R8R27R32R45R39L13L37L40R22L50R49R10L22R3L27L11L34R35L4R1R38R20L2L48R21L15R5R11L37L44L26L30L7R39R50L43L41L22R7L47R7L18R9R30R50L22R37R8R17R45R41R16R23L28L13L7R41L24L7L30R47L15L49L44R33R48L47R38L21L37R2R29L32L13L6R30R42R42L12R8R36R6R13R22R42L44R6R4R19L22R15L27L41L13L26R35L11L15L31R17L34R6R20R41R24L22R40R7L20L20R28L43L15R35R5L41R40L8L25L43R45R39L41R5L17R32R19L21R1R15L8L20R13R46L12R6L16R49L39R43L31R24R29R48L23L19L44R32L25L2L6R11L11L31R39R20R30L7R16L17R42L4L44L8L26L39L41L45L16R37R6L35R33L42L16R50R21L43R22R25L43R46L45L12R40L13L3L9R32R15R21R20L12L4L7L13L48L39L9R19R48R3L31R39R49L35R2R5L33R26R43L11R49R20L30R12L31R43R36R49L30L47R18L9L48R47L11R29L1R45R37L29L50R39L16R27L26L19L21R9R20R28R20R8R2R39R31L2R14L36L39L10R8R40L40R14R32L33L23L38L46R34L19R35R36L20R16L49L17R48R12R15R21L6L45L26L19R43R5R20R19L21L44R31R6R16R49R34L34R49R41R25R47R11L29R34R20L29L35L20L11R15L50L17R2"


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def get_delta(self):
        if self == Direction.RIGHT:
            return 0, 1
        elif self == Direction.DOWN:
            return 1, 0
        elif self == Direction.LEFT:
            return 0, -1
        elif self == Direction.UP:
            return -1, 0

    def turn(self, direction):
        if direction == "R":
            if self == Direction.RIGHT:
                return Direction.DOWN
            elif self == Direction.DOWN:
                return Direction.LEFT
            elif self == Direction.LEFT:
                return Direction.UP
            elif self == Direction.UP:
                return Direction.RIGHT
        else:
            if self == Direction.RIGHT:
                return Direction.UP
            elif self == Direction.UP:
                return Direction.LEFT
            elif self == Direction.LEFT:
                return Direction.DOWN
            elif self == Direction.DOWN:
                return Direction.RIGHT


class Side(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5


    def get_absolute(self, column, row) -> Tuple[int, int]:
        if self == self.A:
            return column + 50, row
        if self == self.B:
            return column + 100, row
        if self == self.C:
            return column + 50, row + 50
        if self == self.D:
            return column + 50, row + 100
        if self == self.E:
            return column, row + 100
        if self == self.F:
            return column, row + 150

    def wrap_around(self, column, row, direction):  # Side, column, row, direction
        if self == self.A:
            if direction == Direction.RIGHT:
                return self.B, 0, row, Direction.RIGHT
            if direction == Direction.DOWN:
                return self.C, column, 0, Direction.DOWN
            if direction == Direction.LEFT:
                return self.E, 0, 49 - row, Direction.RIGHT
            if direction == Direction.UP:
                return self.F, 0, column, Direction.RIGHT

        if self == self.B:
            if direction == Direction.RIGHT:
                return self.D, 49, 49 - row, Direction.LEFT
            if direction == Direction.DOWN:
                return self.C, 49, column, Direction.LEFT
            if direction == Direction.LEFT:
                return self.A, 49, row, Direction.LEFT
            if direction == Direction.UP:
                return self.F, column, 49, Direction.UP

        if self == self.C:
            if direction == Direction.RIGHT:
                return self.B, row, 49, Direction.UP
            if direction == Direction.DOWN:
                return self.D, column, 0, Direction.DOWN
            if direction == Direction.LEFT:
                return self.E, row, 0, Direction.DOWN
            if direction == Direction.UP:
                return self.A, column, 49, Direction.UP

        if self == self.D:
            if direction == Direction.RIGHT:
                return self.B, 49, 49 - row, Direction.LEFT
            if direction == Direction.DOWN:
                return self.F, 49, column, Direction.LEFT
            if direction == Direction.LEFT:
                return self.E, 49, row, Direction.LEFT
            if direction == Direction.UP:
                return self.C, column, 49, Direction.UP

        if self == self.E:
            if direction == Direction.RIGHT:
                return self.D, 0, row, Direction.RIGHT
            if direction == Direction.DOWN:
                return self.F, column, 0, Direction.DOWN
            if direction == Direction.LEFT:
                return self.A, 0, 49 - row, Direction.RIGHT
            if direction == Direction.UP:
                return self.C, 0, column, Direction.RIGHT

        if self == self.F:
            if direction == Direction.RIGHT:
                return self.D, row, 49, Direction.UP
            if direction == Direction.DOWN:
                return self.B, column, 0, Direction.DOWN
            if direction == Direction.LEFT:
                return self.A, row, 0, Direction.DOWN
            if direction == Direction.UP:
                return self.E, column, 49, Direction.UP


def process_data(map: List[str], path: List[Union[str, int]]):
    len_of_strings = max(len(row) for row in map)
    for i in range(len(map)):
        if len(map[i]) < len_of_strings:
            map[i] = map[i] + "".join(" " for i in range(len(map[i]), len_of_strings))

    row = 0
    column = next(i for i, s in enumerate(map[0]) if s == ".")
    direction = Direction.RIGHT

    for path_instruction in path:
        if path_instruction == "L" or path_instruction == "R":
            direction = direction.turn(path_instruction)
            continue

        dy, dx = direction.get_delta()
        for _ in range(path_instruction):
            next_row = row + dy
            next_column = column + dx

            if next_row >= len(map):
                next_row = 0

            if next_row < 0:
                next_row = len(map) - 1

            if next_column >= len(map[next_row]):
                next_column = 0

            if next_column < 0:
                next_column = len(map[next_row]) - 1

            while map[next_row][next_column] == " ":
                next_row += dy
                next_column += dx

                if next_row >= len(map):
                    next_row = 0

                if next_row < 0:
                    next_row = len(map) - 1

                if next_column >= len(map[next_row]):
                    next_column = 0

                if next_column < 0:
                    next_column = len(map[next_row]) - 1

            if map[next_row][next_column] == "#":
                break

            row, column = next_row, next_column

    return row, column, direction


def process_data_2(map: List[str], path: List[Union[str, int]]):
    column = 0
    row = 0
    side = Side.A
    direction = Direction.RIGHT

    for path_instruction in path:
        if path_instruction == "L" or path_instruction == "R":
            direction = direction.turn(path_instruction)
            continue

        print(f"Going {direction} for {path_instruction} steps from ({row}, {column}) on {side}")

        for _ in range(path_instruction):
            dy, dx = direction.get_delta()

            next_side = side
            next_row = row + dy
            next_column = column + dx
            next_direction = direction

            if next_row < 0 or next_row > 49:
                next_side, next_column, next_row, next_direction = side.wrap_around(next_column, next_row, next_direction)
            elif next_column < 0 or next_column > 49:
                next_side, next_column, next_row, next_direction = side.wrap_around(next_column, next_row, next_direction)

            absolute_column, absolute_row = next_side.get_absolute(next_column, next_row)

            if map[absolute_row][absolute_column] == "#":
                break

            side, column, row, direction = next_side, next_column, next_row, next_direction

    absolute_column, absolute_row = side.get_absolute(column, row)
    return absolute_row, absolute_column, direction



def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", do_not_strip=True, is_test=is_test)
    result = process_data(data, parse_instructions(test_path if is_test else real_path))

    # The final password is the sum of 1000 times the row, 4 times the column, and the facing.
    return 1000 * (result[0] + 1) + 4 * (result[1] + 1) + result[2].value


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", do_not_strip=True, is_test=is_test)
    result = process_data_2(data, parse_instructions(test_path if is_test else real_path))

    # The final password is the sum of 1000 times the row, 4 times the column, and the facing.
    return 1000 * (result[0] + 1) + 4 * (result[1] + 1) + result[2].value


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")  # This will only work with the non-test data, because fuck this.
