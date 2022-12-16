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


def process_data(data: List[Tuple[str, int, List[str]]]) -> int:
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

    # Now we need to find the best path still under 30 which only stops at > 0 flow and maximises pressure...
    interesting_nodes = [key for key, value in graph_nodes.items() if value > 0]

    still_to_check = [(30, 0, starting_node)]
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

    all = flatten(all_checked.values())
    best = max(all, key=lambda c: c[1])

    # Rebuild path:
    minute = 1
    flow = 0
    for source, target in zip(best[2].split("-")[:-1], best[2].split("-")[1:]):
        time = dist[(source, target)]
        print(f"At minute {minute} I am at {source} (flow {graph_nodes[source]})")

        if graph_nodes[source] > 0:
            minute += 1
            extra_flow = (30 - minute + 1) * graph_nodes[source]
            flow += extra_flow
            print(f"I am opening {source} until {minute} for and extra {extra_flow} for a final {flow} flow")

        minute += time

    source = best[2].split("-")[-1]
    print(f"At minute {minute} I am at {source} (flow {graph_nodes[source]})")
    if graph_nodes[source] > 0:
        minute += 1
        extra_flow = (30 - minute + 1) * graph_nodes[source]
        flow += extra_flow
        print(f"I am opening {source} until {minute} for and extra {extra_flow} for a final {flow} flow")

    return best


def process_data_2(data: List[Tuple[str, int, List[str]]]) -> int:
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

    # Now we need to find the best path still under 26 which only stops at > 0 flow and maximises pressure...
    # But with an extra elephant!
    interesting_nodes = [key for key, value in graph_nodes.items() if value > 0]

    still_to_check = [((26, 26), 0, (starting_node, starting_node))]
    checked = set()
    all_checked = {(node_1, node_2): [] for node_1 in graph_nodes.keys() for node_2 in graph_nodes.keys()}

    while len(still_to_check) > 0:
        print(f"Stack size is {len(still_to_check)}")
        to_check_now = still_to_check.pop(0)

        if to_check_now in checked:
            continue

        checked.add(to_check_now)
        (me_time_left, other_time_left), final_flow, (me_path_string, other_path_string) = to_check_now
        me_path = me_path_string.split("-")
        other_path = other_path_string.split("-")

        if me_time_left <= 0 or other_time_left <= 0:
            continue

        me_current_node = me_path[-1]
        other_current_node = other_path[-1]

        if len(set(me_current_node + other_current_node)) == len(graph_nodes):
            # We've visited everything, no need to go on
            continue

        all_checked[(me_current_node, other_current_node)].append(to_check_now)

        # Find neighbours
        for me_target in interesting_nodes:
            if me_target in me_path or me_target in other_path:
                continue

            me_distance = dist[(me_current_node, me_target)]
            me_target_flow = graph_nodes[me_target]

            # Open, because if you didn't want to open it, you shouldn't have passed by here
            me_new_time_left = me_time_left - me_distance - 1
            me_extra_flow = me_new_time_left * me_target_flow
            me_new_path_string = me_path_string + "-" + me_target

            for other_target in interesting_nodes:
                if other_target in other_path or other_target in me_path or other_target == me_target:
                    continue

                other_distance = dist[(other_current_node, other_target)]
                other_target_flow = graph_nodes[other_target]

                # Open, because if you didn't want to open it, you shouldn't have passed by here
                other_new_time_left = other_time_left - other_distance - 1
                other_extra_flow = other_new_time_left * other_target_flow
                other_new_path_string = other_path_string + "-" + other_target

                new_final_flow = final_flow + me_extra_flow + other_extra_flow

                new_to_search = (me_new_time_left, other_new_time_left), new_final_flow, (me_new_path_string, other_new_path_string)
                still_to_check.insert(0, new_to_search)

    all = flatten(all_checked.values())
    best = max(all, key=lambda c: c[1])
    #
    # # Rebuild path:
    # minute = 1
    # flow = 0
    # for source, target in zip(best[2].split("-")[:-1], best[2].split("-")[1:]):
    #     time = dist[(source, target)]
    #     print(f"At minute {minute} I am at {source} (flow {graph_nodes[source]})")
    #
    #     if graph_nodes[source] > 0:
    #         minute += 1
    #         extra_flow = (26 - minute + 1) * graph_nodes[source]
    #         flow += extra_flow
    #         print(f"I am opening {source} until {minute} for and extra {extra_flow} for a final {flow} flow")
    #
    #     minute += time
    #
    # source = best[2].split("-")[-1]
    # print(f"At minute {minute} I am at {source} (flow {graph_nodes[source]})")
    # if graph_nodes[source] > 0:
    #     minute += 1
    #     extra_flow = (26 - minute + 1) * graph_nodes[source]
    #     flow += extra_flow
    #     print(f"I am opening {source} until {minute} for and extra {extra_flow} for a final {flow} flow")

    return best


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    return result


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data_2(data)
    return result


if __name__ == '__main__':
    is_test = False
    # print(f"Day {DAY} result 1: {part_1(is_test)}")  # 1897 is too high! 1885 is also too high. 1882 is also too high!
    print(f"Day {DAY} result 2: {part_2(is_test)}")
