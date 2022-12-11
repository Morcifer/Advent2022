import math
from typing import List, Optional, Tuple, Dict

from src.utilities import load_data

DAY = 11


class Monkey:
    def __init__(
        self,
        number,
        items,
        worry_operation,
        test,
        monkey_on_true,
        monkey_on_false,
    ):
        self.number = number
        self.items = items
        self.worry_operation = worry_operation
        self.test = test
        self.on_true = monkey_on_true
        self.on_false = monkey_on_false

    def new_monkey_new_worry(self, worry_level_before_inspection):
        worry_level_after_inspection = self.worry_operation(worry_level_before_inspection)
        # worry_level_after_boredom = int(math.floor(worry_level_after_inspection/3.0))
        # worry_level_after_boredom = worry_level_after_inspection % (23*19*13*17)
        worry_level_after_boredom = worry_level_after_inspection % (19*2*3*17*13*7*5*11)
        if self.test(worry_level_after_boredom):
            return self.on_true, worry_level_after_boredom

        return self.on_false, worry_level_after_boredom


def parser(s: List[List[str]]) -> Monkey:
    # Monkey 0:
    #   Starting items: 79, 98
    #   Operation: new = old * 19
    #   Test: divisible by 23
    #     If true: throw to monkey 2
    #     If false: throw to monkey 3
    worry_operation_line = s[2]
    operation = worry_operation_line[4]
    second_value = worry_operation_line[5]

    if operation == "+":
        if second_value == "old":
            worry_operation = lambda x: x + x
        else:
            worry_operation = lambda x: x + int(second_value)

    elif operation == "*":
        if second_value == "old":
            worry_operation = lambda x: x * x
        else:
            worry_operation = lambda x: x * int(second_value)
    else:
        raise ValueError

    return Monkey(
        number=int(s[0][1][0]),
        items=[int(x.replace(",", "")) for x in s[1][2:]],
        worry_operation=worry_operation,
        test=lambda x: (x % int(s[3][-1])) == 0,
        monkey_on_true=int(s[4][-1]),
        monkey_on_false=int(s[5][-1]),
    )


def process_data(monkeys: List[Monkey]) -> Dict[int, int]:
    inspections = {monkey.number: 0 for monkey in monkeys}

    for round in range(10000):
        # print(f"round {round}")
        for monkey in monkeys:
            inspections[monkey.number] += len(monkey.items)
            for item in monkey.items:
                new_monkey, new_worry = monkey.new_monkey_new_worry(item)
                monkeys[new_monkey].items.append(new_worry)
            monkey.items = []

    return inspections


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test, cluster_lines=7)
    result = process_data(data)
    inspections = sorted(list(result.values()))[-2:]
    return inspections[0] * inspections[1]


def part_2(is_test: bool) -> None:
    data = load_data(DAY, parser, "data", is_test=is_test, cluster_lines=7)
    result = process_data(data)
    return None


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    # print(f"Day {DAY} result 2: {part_2(is_test)}")
