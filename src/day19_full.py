import itertools
import math
import random
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from functools import partial, cmp_to_key
from typing import List, Optional, Tuple, Dict, Set

from src.utilities import load_data

DAY = 19


def flatten(sequence):
    return list(itertools.chain(*sequence))


class OreType(Enum):
    NONE = 0,
    ORE = 1,
    CLAY = 2,
    OBSIDIAN = 3,
    GEODE = 4,

    @classmethod
    def all_ore_types(cls) -> List['OreType']:
        return [cls.GEODE, cls.ORE, cls.CLAY, cls.OBSIDIAN]


@dataclass
class Factory:
    identifier: int
    robot_costs: Dict[OreType, Dict[OreType, int]]

    @property
    def max_cost_per_type(self):
        return {
            cost_ore_type: max(robot_costs.get(cost_ore_type, 0) for _, robot_costs in self.robot_costs.items())
            for cost_ore_type in OreType.all_ore_types()
        }


@dataclass
class RobotState:
    robots: dict

    def get_hash_str(self, ore_amount):
        robots_str = "-".join(str(self.robots[ore_type]) for ore_type in OreType.all_ore_types())
        ore_amount_str = "-".join(str(ore_amount[ore_type]) for ore_type in OreType.all_ore_types())

        return f"{robots_str}_{ore_amount_str}"

    def get_minute_hash_str(self, minute, ore_amount):
        minute_str = str(minute)
        robots_str = "-".join(str(self.robots[ore_type]) for ore_type in OreType.all_ore_types())
        ore_amount_str = "-".join(str(ore_amount[ore_type]) for ore_type in OreType.all_ore_types())

        return f"{minute_str}_{robots_str}_{ore_amount_str}"

    def get_extra_ores(self, old_ores: dict) -> dict:
        return {
            ore_type: old_amount + self.robots[ore_type]
            for ore_type, old_amount
            in old_ores.items()
        }

    def make_one_robot(
        self,
        robot_ore_type: OreType,
        old_ores: dict,
        factory: Factory
    ) -> Optional[Tuple[int, dict, dict]]:
        max_turns = 0

        for cost_ore_type in OreType.all_ore_types():
            if old_ores[cost_ore_type] < factory.robot_costs[robot_ore_type].get(cost_ore_type, 0):
                if self.robots[cost_ore_type] >= 1:
                    turns_for_this_ore = 1.0 * factory.robot_costs[robot_ore_type].get(cost_ore_type, 0) / self.robots[cost_ore_type]
                    max_turns = max(max_turns, int(math.ceil(turns_for_this_ore)))
                else:
                    return None

        if robot_ore_type != OreType.GEODE and self.robots[robot_ore_type] >= factory.max_cost_per_type[robot_ore_type]:
            return None

        new_ores = {
            cost_ore_type: amount_old_ore + self.robots[cost_ore_type] * max_turns - factory.robot_costs[robot_ore_type].get(cost_ore_type, 0)
            for cost_ore_type, amount_old_ore
            in old_ores.items()
        }

        new_robots = self.robots.copy()
        new_robots[robot_ore_type] += 1

        return max_turns, new_ores, new_robots


def parser(s: List[str]) -> Factory:
    # Blueprint 1: Each ore robot costs 4 ore.
    # Each clay robot costs 2 ore.
    # Each obsidian robot costs 3 ore and 14 clay.
    # Each geode robot costs 2 ore and 7 obsidian.
    return Factory(
        identifier=int(s[1].replace(":", "")),
        robot_costs={
            OreType.ORE: {OreType.ORE: int(s[6])},
            OreType.CLAY: {OreType.ORE: int(s[12])},
            OreType.OBSIDIAN: {OreType.ORE: int(s[18]), OreType.CLAY: int(s[21])},
            OreType.GEODE: {OreType.ORE: int(s[27]), OreType.OBSIDIAN: int(s[30])}
        },
    )


default_robots = {
    OreType.ORE: 1,
    OreType.CLAY: 0,
    OreType.OBSIDIAN: 0,
    OreType.GEODE: 0,
}


def process_data(data: List[Factory], minutes: int) -> Dict[int, int]:
    result = {}

    for factory in data:
        print(f"Factory {factory.identifier}, results thus far {result}")
        result[factory.identifier] = []

        money_state = {ore_type: 0 for ore_type in OreType.all_ore_types()}
        robot_state = RobotState(robots=default_robots.copy())

        states_to_check = [(0, money_state, robot_state)]
        checked_hashes = set()
        finished_states = []

        best_state_per_minutes = {}
        best_geode = 0

        while len(states_to_check) > 0:
            minute, money_state, robot_state = states_to_check.pop(-1)
            hash_to_check = robot_state.get_minute_hash_str(minute, money_state)

            if hash_to_check in checked_hashes:
                continue

            checked_hashes.add(hash_to_check)

            if minute > minutes:
                continue

            if minute == minutes:
                finished_states.append(money_state)

                if money_state[OreType.GEODE] > best_geode:
                    print(f"Still {len(states_to_check)} to check, current best geode is {money_state[OreType.GEODE]}")

                best_geode = max(best_geode, money_state[OreType.GEODE])
                continue

            if minute not in best_state_per_minutes:
                best_state_per_minutes[minute] = (money_state, robot_state)
            else:
                best_money_state, best_robot_state = best_state_per_minutes[minute]

                if all(
                    money_state[ore_type] >= best_money_state[ore_type] and robot_state.robots[ore_type] >= best_robot_state.robots[ore_type]
                    for ore_type in OreType.all_ore_types()
                ):
                    best_state_per_minutes[minute] = (money_state, robot_state)
                elif all(
                        money_state[ore_type] <= best_money_state[ore_type] and robot_state.robots[ore_type] <= best_robot_state.robots[ore_type]
                        for ore_type in OreType.all_ore_types()
                ):
                    continue

            # Build robots
            robot_options = {}

            for robot_ore_type in OreType.all_ore_types():
                new_possibility = robot_state.make_one_robot(robot_ore_type, money_state, factory)

                if new_possibility is None:  # Not enough money
                    continue
                else:
                    extra_turns, new_ores, new_robots = new_possibility

                    if new_robots is not None:  # This is a good robot to build
                        new_state = (
                            minute + extra_turns + 1,
                            robot_state.get_extra_ores(new_ores),
                            RobotState(robots=new_robots)
                        )
                        robot_options[robot_ore_type] = new_state

            if OreType.GEODE in robot_options and robot_options[OreType.GEODE][0] == minute + 1:
                states_to_check.append(robot_options[OreType.GEODE])
            else:
                states_to_check.extend(robot_options.values())

        result[factory.identifier] = max(money[OreType.GEODE] for money in finished_states)

    return result


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, minutes=24)
    print("Result: ", result)  # Test should be {1: 9, 2: 12}

    return sum(
        identifier * geodes
        for identifier, geodes in result.items()
    )


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)

    result = process_data(data[:3], minutes=32)
    print("Result: ", result)  # Test should be {1: 56, 2: 62}

    return result.get(1, 1) * result.get(2, 1) * result.get(3, 1)


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")  # part 1: 817, part 2: 4216
    print(f"Day {DAY} result 2: {part_2(is_test)}")
