from collections import defaultdict
import math
import functools
import networkx as nx

Graph = dict[str, set[str]]


def to_nx_graph(graph):
    nx_graph = nx.Graph()
    for node, adj_nodes in graph.items():
        nx_graph.add_node(node)
        nx_graph.add_edges_from([(node, adj_node) for adj_node in adj_nodes])
    return nx_graph


def get_filtered_graph(graph, filter_fn):
    new_graph = dict()

    for node, adj_nodes in graph.items():
        if filter_fn(node):
            new_graph[node] = {e for e in adj_nodes if filter_fn(e)}
    return new_graph


def read_graph_from_file(fname):
    graph = defaultdict(set)
    with open(fname) as f:
        for line in f:
            line = line.strip()
            n1 = line[:2]
            n2 = line[3:]
            graph[n1].add(n2)
            graph[n2].add(n1)
    return graph


def count_special_cliques(graph):
    # a special clique is a clique of size 3 in which at least 1 node starts with t
    nx_graph = to_nx_graph(graph)
    total = 0
    cliques = list(nx.find_cliques(nx_graph))
    for clique in cliques:
        n_nodes = len(clique)
        if n_nodes > 3:
            n_t_nodes = len([x for x in clique if x[0] == "t"])
            for i in range(1, min(n_t_nodes, 3) + 1):
                total += math.comb(n_t_nodes, i) * math.comb(n_nodes - n_t_nodes, 3 - i)
    return total


def part1(graph):
    def filter_fn(node, graph):
        return node[0] == "t" or any([n[0] == "t" for n in graph[node]])

    filtered_graph = get_filtered_graph(
        graph, functools.partial(filter_fn, graph=graph)
    )
    print(count_special_cliques(filtered_graph))
