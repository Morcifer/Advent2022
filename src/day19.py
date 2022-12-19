import itertools
import math
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

    def all_ore_types(self) -> List['OreType']:
        return [self.ORE, self.CLAY, self.OBSIDIAN, self.GEODE]


@dataclass
class Factory:
    identifier: int
    robot_costs: Dict[OreType, Dict[OreType, int]]


@dataclass
class RobotState:
    robots = {
        OreType.ORE: 1,
        OreType.CLAY: 0,
        OreType.OBSIDIAN: 0,
        OreType.GEODE: 0,
    }

    def get_extra_ores(self, old_ores: dict) -> dict:
        return {ore_type: old_amount + self.robots[ore_type] for ore_type, old_amount in old_ores}

    def make_one_robot(
        self,
        robot_ore_type: OreType,
        old_ores: dict,
        factory: Factory
    ) -> Tuple[Optional[dict], dict]:
        for cost_ore_type in robot_ore_type.all_ore_types():
            if old_ores[cost_ore_type] < factory.robot_costs[robot_ore_type][cost_ore_type]:
                return None, old_ores.copy()

        new_ores = {
            cost_ore_type: amount_old_ore - factory.robot_costs[robot_ore_type][cost_ore_type]
            for cost_ore_type, amount_old_ore
            in old_ores
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


def process_data(data: List[Factory], minutes: int) -> Dict[int, int]:
    for factory in data:
        # Each robot can collect 1 of its resource type per minute.
        # It also takes one minute for the robot factory (also conveniently from your pack) to construct any type of robot,
        # although it consumes the necessary resources available when construction begins.

        print(factory)
    return {}


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, minutes=24)
    return sum(identifier * geodes for identifier, geodes  in result)


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
