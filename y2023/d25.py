import networkx as nx


def parse_graph(fname) -> nx.Graph:
    nodes = set()
    edges = set()
    with open(fname) as f:
        for line in f:
            line = line.strip()
            node, neighbors_str = line.split(": ")
            nodes.add(node)
            for neighbor in neighbors_str.split(" "):
                nodes.add(neighbor)
                edges.add((node, neighbor))
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    return g


def part1(fname):
    graph = parse_graph(fname)
    edges_to_remove = nx.minimum_edge_cut(graph)
    assert len(edges_to_remove) == 3
    graph.remove_edges_from(edges_to_remove)
    connected_subgraphs = list(nx.connected_components(graph))
    assert len(connected_subgraphs) == 2
    return len(connected_subgraphs[0]) * len(connected_subgraphs[1])


if __name__ == "__main__":
    part1("./y2023/data/d25_small.txt")
    part1("./y2023/data/d25.txt")
