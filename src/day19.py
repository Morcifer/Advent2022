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
    ORE = 0,
    CLAY = 1,
    OBSIDIAN = 2,
    GEODE = 3,

    @classmethod
    def all_ore_types(cls) -> List['OreType']:
        return [cls.ORE, cls.CLAY, cls.OBSIDIAN, cls.GEODE]


@dataclass
class Factory:
    identifier: int
    robot_costs: Dict[OreType, Dict[OreType, int]]


@dataclass
class RobotState:
    robots: dict

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

        if self.robots[OreType.CLAY] == 0 and (robot_ore_type == OreType.OBSIDIAN or robot_ore_type == OreType.GEODE):
            return None, None

        if robot_ore_type == OreType.GEODE and self.robots[OreType.OBSIDIAN] == 0:
            return None, None

        new_ores = {
            cost_ore_type: amount_old_ore - factory.robot_costs[robot_ore_type].get(cost_ore_type, 0)
            for cost_ore_type, amount_old_ore
            in old_ores.items()
        }

        new_robots = self.robots.copy()
        new_robots[robot_ore_type] += 1

        return new_robots, new_ores


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
        print(f"Working on factory {factory.identifier}")
        result[factory.identifier] = []

        for random_id in range(1000):
            money_state = {ore_type: 0 for ore_type in OreType.all_ore_types()}
            robot_state = RobotState(robots=default_robots.copy())

            for minute in range(minutes):
                # print(f"Working minute {minute} for factory {factory.identifier}, random game id {random_id}")

                # Each robot can collect 1 of its resource type per minute.
                money_state = robot_state.get_extra_ores(money_state)

                # Do nothing
                possible_new_states = [(money_state, robot_state)]

                for robot_ore_type in OreType.all_ore_types():
                    new_robots, new_ores = robot_state.make_one_robot(robot_ore_type, money_state, factory)

                    if new_robots is not None:
                        new_game_state = (new_ores, RobotState(robots=new_robots))
                        possible_new_states.append(new_game_state)

                random_draw = random.sample(possible_new_states, 1)[0]
                money_state, robot_state = random_draw

            result[factory.identifier].append(money_state[OreType.GEODE])

    return {identifier: max(values) for identifier, values in result.items()}


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, minutes=24)
    print(result)  # Should be {1: 9, 2: 12}
    return sum(identifier * geodes for identifier, geodes in result.items())


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
