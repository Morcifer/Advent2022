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


def process_data(data: List[Tuple[str, int, List[str]]]) -> List[Tuple[int, int]]:
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
    interesting_distances = {
        key: value
        for key, value in dist.items()
        if graph_nodes[key[0]] > 0 and graph_nodes[key[1]] > 0
    }

    # procedure DFS_iterative(G, v) is
    #     let S be a stack
    #     S.push(v)
    #     while S is not empty do
    #         v = S.pop()
    #         if v is not labeled as discovered then
    #             label v as discovered
    #             for all edges from v to w in G.adjacentEdges(v) do
    #                 S.push(w)
    # discovered
    # s = []
    # s.insert(0, starting_node)
    # while len(s) > 0:
    #     v = s.pop(0)


    return process_data



def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    return sum((30 - minute) * pressure for minute, pressure in result)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    result = process_data(data)
    return sum((30 - minute) * pressure for minute, pressure in result)


if __name__ == '__main__':
    is_test = True
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
