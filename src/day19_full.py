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
        return [cls.ORE, cls.CLAY, cls.OBSIDIAN, cls.GEODE]


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
    ) -> Tuple[Optional[dict], Optional[dict]]:
        for cost_ore_type in OreType.all_ore_types():
            if old_ores[cost_ore_type] < factory.robot_costs[robot_ore_type].get(cost_ore_type, 0):
                return None, None

        if robot_ore_type != OreType.GEODE and self.robots[robot_ore_type] >= factory.max_cost_per_type[robot_ore_type]:
            return None, None

        new_ores = {
            cost_ore_type: amount_old_ore - factory.robot_costs[robot_ore_type].get(cost_ore_type, 0)
            for cost_ore_type, amount_old_ore
            in old_ores.items()
        }

        new_robots = self.robots.copy()
        new_robots[robot_ore_type] += 1

        return new_ores, new_robots


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
        result[factory.identifier] = []

        money_state = {ore_type: 0 for ore_type in OreType.all_ore_types()}
        robot_state = RobotState(robots=default_robots.copy())

        states_to_check = [(money_state, robot_state)]

        for minute in range(minutes):
            print(f"Minute {minute} for factory {factory.identifier}")

            checked = set()
            new_states_to_check = []

            for money_state, robot_state in states_to_check:
                hash_to_check = robot_state.get_hash_str(money_state)

                if hash_to_check in checked:
                    continue

                checked.add(hash_to_check)

                # Do nothing
                new_states_to_check.append(
                    (
                        robot_state.get_extra_ores(money_state),
                        robot_state
                    )
                )

                # Build robot
                for robot_ore_type in OreType.all_ore_types():
                    new_ores, new_robots = robot_state.make_one_robot(robot_ore_type, money_state, factory)

                    if new_robots is not None:
                        new_state = (
                            robot_state.get_extra_ores(new_ores),
                            RobotState(robots=new_robots)
                        )
                        new_states_to_check.append(new_state)

            states_to_check = new_states_to_check

        result[factory.identifier] = max(money[OreType.GEODE] for money, robots in states_to_check)

    return result


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, minutes=24)
    print("Result: ", result)  # Should be {1: 9, 2: 12}

    return sum(  # 725 is best right now. But it's pretty bad.
        identifier * geodes
        for identifier, geodes in result.items()
    )

# def part_2(is_test: bool) -> int:
#     data = load_data(DAY, parser, "data", is_test=is_test)
#     all_surface_area = process_data(data)
#     internal_cubes = process_data_2(data)
#     internal_surface_area = process_data(internal_cubes)
#
#     return all_surface_area - internal_surface_area


if __name__ == '__main__':
    is_test = True
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    # print(f"Day {DAY} result 2: {part_2(is_test)}")
