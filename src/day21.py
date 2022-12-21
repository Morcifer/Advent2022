import itertools
import math
from copy import deepcopy
from functools import partial, cmp_to_key
from typing import List, Optional, Tuple, Dict, Set, Union

from src.utilities import load_data

DAY = 21


def flatten(sequence):
    return list(itertools.chain(*sequence))


def parser(s: List[str]) -> Tuple[str, Union[int, Tuple[str, str, str]]]:
    monkey = s[0].replace(":", "")
    return (monkey, int(s[1])) if len(s) == 2 else (monkey, (s[1], s[2], s[3]))


def process_data(data: List[int]):
    return {monkey: command for monkey, command in data}


def process_data_2(commands):
    commands["humn"] = "x"

    split_monkey = "root"

    left_value = find_value_of_monkey(commands, commands[split_monkey][0])
    right_value = find_value_of_monkey(commands, commands[split_monkey][2])

    value_to_equal = left_value if isinstance(left_value, int) else right_value
    monkey_to_check = commands[split_monkey][2] if value_to_equal == left_value else commands[split_monkey][0]

    while True:
        left_value = find_value_of_monkey(commands, commands[monkey_to_check][0])
        right_value = find_value_of_monkey(commands, commands[monkey_to_check][2])

        expression = commands[monkey_to_check][1]

        if isinstance(left_value, int):
            if expression == "+":
                value_to_equal -= left_value
            elif expression == "*":
                value_to_equal = int(value_to_equal / left_value)
            elif expression == "-":
                value_to_equal = left_value - value_to_equal
            elif expression == "/":
                value_to_equal = int(left_value / value_to_equal)

            if right_value == "x":
                return value_to_equal

            monkey_to_check = commands[monkey_to_check][2]
        else:
            if expression == "+":
                value_to_equal -= right_value
            elif expression == "*":
                value_to_equal = int(value_to_equal / right_value)
            elif expression == "-":
                value_to_equal += right_value
            elif expression == "/":
                value_to_equal *= right_value

            if left_value == "x":
                return value_to_equal

            monkey_to_check = commands[monkey_to_check][0]


def find_value_of_monkey(commands, monkey):
    if isinstance(commands[monkey], int):
        return commands[monkey]

    if monkey == "humn":
        return commands[monkey]

    left_value = find_value_of_monkey(commands, commands[monkey][0])
    right_value = find_value_of_monkey(commands, commands[monkey][2])

    if isinstance(left_value, int) and isinstance(right_value, int):
        to_eval = f"{left_value}{commands[monkey][1]}{right_value}"
        return int(eval(to_eval))

    to_calculate = f"({left_value}){commands[monkey][1]}({right_value})"
    return to_calculate


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    commands = process_data(data)
    return find_value_of_monkey(commands, "root")


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    commands = process_data(data)
    result = process_data_2(commands)
    return result


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
