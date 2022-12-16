import itertools
from functools import partial, cmp_to_key
from typing import List, Optional, Tuple, Dict, Set

from src.utilities import load_data

DAY = 16


def flatten(sequence):
    return list(itertools.chain(*sequence))


def parser(s: List[str]) -> Tuple[str, int, List[str]]:
    # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    def get_int(substring):
        return int(
            substring
                .replace(",", "")
                .replace(":", "")
                .replace(";", "")
                .split("=")
            [1]
        )

    return s[1], get_int(s[4]), [c.replace(",", "") for c in s[9:]]


def process_data(data: List[Tuple[str, int, List[str]]], time_to_open) -> List[Tuple[int, str]]:
    graph_nodes = {}
    graph_edges = {}

    starting_node = "AA"

    for node, rate, edges in data:
        graph_nodes[node] = rate
        graph_edges[node] = edges

    # First figure out how long it takes to get from each >0 node to another with Floyd–Warshall
    dist = {
        (node_1, node_2): float('inf')
        for node_1 in graph_nodes.keys()
        for node_2 in graph_nodes.keys()
    }
    for source, targets in graph_edges.items():
        for target in targets:
            dist[(source, target)] = 1

    for node in graph_nodes:
        dist[(node, node)] = 0

    for node_k in graph_nodes.keys():
        for node_i in graph_nodes.keys():
            for node_j in graph_nodes.keys():
                if dist[(node_i, node_j)] > dist[(node_i, node_k)] + dist[(node_k, node_j)]:
                    dist[(node_i, node_j)] = dist[(node_i, node_k)] + dist[(node_k, node_j)]

    # Now we need to find the best path still under time_to_open/30 which only stops at > 0 flow and maximises pressure...
    interesting_nodes = [key for key, value in graph_nodes.items() if value > 0]

    still_to_check = [(time_to_open, 0, starting_node)]
    checked = set()
    all_checked = {node: [] for node in graph_nodes.keys()}

    while len(still_to_check) > 0:
        to_check_now = still_to_check.pop(0)

        if to_check_now in checked:
            continue

        checked.add(to_check_now)
        time_left, final_flow, path_string = to_check_now
        path = path_string.split("-")

        if time_left <= 0:
            continue

        current_node = path[-1]

        if len(path) == len(graph_nodes):
            # We've visited everything, no need to go on
            continue

        all_checked[current_node].append(to_check_now)

        # Find neighbours
        for target in interesting_nodes:
            if target in path:
                continue

            distance = dist[(current_node, target)]
            target_flow = graph_nodes[target]

            # Open, because if you didn't want to open it, you shouldn't have passed by here
            new_time_left = time_left - distance - 1
            extra_flow = new_time_left * target_flow
            new_final_flow = final_flow + extra_flow
            new_path_string = path_string + "-" + target

            new_to_search = new_time_left, new_final_flow, new_path_string
            still_to_check.insert(0, new_to_search)

    return [(flow, path) for time, flow, path in flatten(all_checked.values())]


def process_data_2(all_possibilities: List[Tuple[int, str]]) -> Tuple[Tuple[int, str], Tuple[int, str]]:
    all_possibilities = sorted(all_possibilities, key=lambda x: -x[0])
    all_possibilities = all_possibilities[:5000]

    all_pairs = [
        (solution_1, solution_2)
        for solution_1 in all_possibilities
        for solution_2 in all_possibilities
        if len(set(solution_1[1].split("-")).intersection(solution_2[1].split("-"))) == 1
    ]

    return max(all_pairs, key=lambda s: s[0][0] + s[1][0])


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data, time_to_open=30)
    return max(result, key=lambda c: c[0])[0]


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    all_options = process_data(data, time_to_open=26)
    result = process_data_2(all_options)
    return result[0][0] + result[1][0]


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
