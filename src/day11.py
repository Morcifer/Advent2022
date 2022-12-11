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
        test_divisor,
        monkey_on_true,
        monkey_on_false,
    ):
        self.number = number
        self.items = items
        self.worry_operation = worry_operation
        self.test_divisor = test_divisor
        self.on_true = monkey_on_true
        self.on_false = monkey_on_false

    def new_monkey_new_worry(self, worry_level_before_inspection, worry_divisor, global_divisor):
        worry_level_after_inspection = self.worry_operation(worry_level_before_inspection)
        valid_modulu = int(global_divisor * worry_divisor)
        worry_level_after_boredom = int(math.floor(worry_level_after_inspection/worry_divisor)) % valid_modulu
        if (worry_level_after_boredom % self.test_divisor) == 0:
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
        test_divisor=int(s[3][-1]),
        monkey_on_true=int(s[4][-1]),
        monkey_on_false=int(s[5][-1]),
    )


def process_data(monkeys: List[Monkey], rounds: int, worry_divisor: float) -> Dict[int, int]:
    inspections = {monkey.number: 0 for monkey in monkeys}
    global_divisor = math.prod(monkey.test_divisor for monkey in monkeys)

    for _ in range(rounds):
        for monkey in monkeys:
            inspections[monkey.number] += len(monkey.items)
            for item in monkey.items:
                new_monkey, new_worry = monkey.new_monkey_new_worry(
                    worry_level_before_inspection=item,
                    worry_divisor=worry_divisor,
                    global_divisor=global_divisor,
                )
                monkeys[new_monkey].items.append(new_worry)
            monkey.items = []

    return inspections


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test, cluster_lines=7)
    result = process_data(data, rounds=20, worry_divisor=3.0)
    inspections = sorted(list(result.values()))[-2:]
    return inspections[0] * inspections[1]


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test, cluster_lines=7)
    result = process_data(data, rounds=10000, worry_divisor=1.0)
    inspections = sorted(list(result.values()))[-2:]
    return inspections[0] * inspections[1]


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
