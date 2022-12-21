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
    commands = {monkey: command for monkey, command in data}

    nodes = {monkey: command if isinstance(command, int) else command[1] for monkey, command in commands.items()}
    edges = {monkey: [] for monkey in commands.keys()}

    leaves = {}

    for monkey, command in commands.items():
        if isinstance(command, int):
            leaves[monkey] = command
        else:
            edges[monkey].append(command[0])
            edges[monkey].append(command[2])

    return nodes, edges


def process_data_2(nodes, edges):
    for value_to_yell in range(6000, 50000):
        nodes["humn"] = value_to_yell
        left_value = find_value_of_monkey(nodes, edges, edges["root"][0])
        right_value = find_value_of_monkey(nodes, edges, edges["root"][1])

        if left_value == right_value:
            return value_to_yell

        if value_to_yell % 1000 == 0:
            print(f"Yelling values up to {value_to_yell} didn't work.")

    return -1


def find_value_of_monkey(nodes, edges, monkey):
    if isinstance(nodes[monkey], int):
        return nodes[monkey]

    branches = edges[monkey]
    left_value = find_value_of_monkey(nodes, edges, branches[0])
    right_value = find_value_of_monkey(nodes, edges, branches[1])

    to_eval = f"{left_value}{nodes[monkey]}{right_value}"
    result = eval(to_eval)

    # print(f"monkey {monkey} has value {result}")

    return result


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    nodes, edges = process_data(data)
    return find_value_of_monkey(nodes, edges, "root")


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    nodes, edges = process_data(data)
    result = process_data_2(nodes, edges)
    return result


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
