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

    starting_node = data[0][0]

    for node, rate, edges in data:
        graph_nodes[node] = rate
        graph_edges[node] = edges

    # First figure out how long it takes to get from each >0 node to another with Floyd–Warshall
    # let dist be a |V| × |V| array of minimum distances initialized to ∞ (infinity)
    dist = {
        (node_1, node_2): float('inf')
        for node_1 in graph_nodes.keys()
        for node_2 in graph_nodes.keys()
    }
    # for each edge (u, v) do
    #     dist[u][v] ← w(u, v)  // The weight of the edge (u, v)
    for source, targets in graph_edges.items():
        for target in targets:
            dist[(source, target)] = 1

    # for each vertex v do
    #     dist[v][v] ← 0
    for node in graph_nodes:
        dist[(node, node)] = 0

    # for k from 1 to |V|
    #     for i from 1 to |V|
    #         for j from 1 to |V|
    #             if dist[i][j] > dist[i][k] + dist[k][j]
    #                 dist[i][j] ← dist[i][k] + dist[k][j]
    #             end if
    for node_k in graph_nodes.keys():
        for node_i in graph_nodes.keys():
            for node_j in graph_nodes.keys():
                if dist[(node_i, node_j)] > dist[(node_i, node_k)] + dist[(node_k, node_j)]:
                    dist[(node_i, node_j)] = dist[(node_i, node_k)] + dist[(node_k, node_j)]

    # Now we need to find the best path still under 30 which only stops at > 0 flow and maximises pressure...
    interesting_nodes = [key for key, value in graph_nodes.items() if value > 0]
    interesting_distances = {
        key: value
        for key, value in dist.items()
        if key[0] in interesting_nodes and key[1] in interesting_nodes
    }

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

        if path_string == "AA-DD-BB-JJ-HH":
            print("?")

        if time_left < 0:
            continue

        current_node = path[-1]
        current_flow = graph_nodes[current_node]

        there_is_already_better = False

        if len(path) == len(graph_nodes):
            # We've visited everything, no need to go on
            continue

        # for possible_better_checked in all_checked[current_node]:
        #     possible_better_time_left, possible_better_final_flow, _ = possible_better_checked
        #
        #     if possible_better_time_left > time_left and possible_better_final_flow > final_flow:
        #         there_is_already_better = True
        #
        # if there_is_already_better:
        #     continue

        all_checked[current_node].append(to_check_now)

        # Find neighbours
        if current_flow > 0:
            # Only go to the good ones!
            for target in interesting_nodes:
                if target in path:
                    continue

                distance = interesting_distances[(current_node, target)]
            # for (source, target), distance in interesting_distances.items():
                target_flow = graph_nodes[target]
                # if source == current_node and target not in path and target_flow > 0:
                if path_string == "AA-DD-BB-JJ" and target == "HH":
                    print(f"?")

                # Open, because if you didn't want to open it, you shouldn't have passed by here
                new_time_left = time_left - distance - 1
                extra_flow = new_time_left * target_flow
                new_final_flow = final_flow + extra_flow
                new_path_string = path_string + "-" + target

                if new_path_string in "AA-DD-BB-JJ-HH-EE-CC":
                    print(f"flow with {new_path_string} is {new_final_flow}")

                new_to_search = new_time_left, new_final_flow, new_path_string
                still_to_check.insert(0, new_to_search)
        elif current_node == starting_node:  # This is only allowed to get out of the first one...
            for target in interesting_nodes:
                distance = dist[(current_node, target)]
                target_flow = graph_nodes[target]

                # Open, because if you didn't want to open it, you shouldn't have passed by here
                new_time_left = time_left - distance - 1
                extra_flow = new_time_left * target_flow
                new_final_flow = final_flow + extra_flow
                new_path_string = path_string + "-" + target

                if new_path_string in "AA-DD-BB-JJ-HH-EE-CC":
                    print(f"flow with {new_path_string} is {new_final_flow}")

                new_to_search = new_time_left, new_final_flow, new_path_string
                still_to_check.insert(0, new_to_search)

    all = flatten(all_checked.values())
    best = max(all, key=lambda c: c[1])

    # Rebuild path:
    minute = 1
    flow = 0
    for source, target in zip(best[2].split("-")[:-1], best[2].split("-")[1:]):
        time = dist[(source, target)]
        print(f"At minute {minute} I am at {source}")

        if graph_nodes[source] > 0:
            minute += 1
            extra_flow = (30 - minute + 1) * graph_nodes[source]
            flow += extra_flow
            print(f"I am opening {source} until {minute} for and extra {extra_flow} for a final {flow} flow")

        minute += time

    source = best[2].split("-")[-1]
    print(f"At minute {minute} I am at {source}")
    if graph_nodes[source] > 0:
        minute += 1
        extra_flow = (30 - minute + 1) * graph_nodes[source]
        flow += extra_flow
        print(f"I am opening {source} until {minute} for and extra {extra_flow} for a final {flow} flow")

    return best


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    return result


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    return sum((30 - minute) * pressure for minute, pressure in result)


if __name__ == '__main__':
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")  # 1897 is too high! 1885 is also too high. 1882 is also too high!
    # print(f"Day {DAY} result 2: {part_2(is_test)}")
