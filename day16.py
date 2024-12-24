from dataclasses import dataclass

from utils import V2, DirectionEnum, Grid, read_grid
import networkx as nx
import math


@dataclass(frozen=True)
class Node:
    p: V2
    direction: DirectionEnum


class Weight:
    ROTATE = 1000
    MOVE = 1


def parse_graph(grid: Grid) -> nx.DiGraph:
    graph = nx.DiGraph()
    for i in range(grid.height):
        for j in range(grid.width):
            p = V2(i, j)
            if grid.at(p) != "#":
                for direction in DirectionEnum:
                    n = Node(p, direction)
                    graph.add_node(n)
                    graph.add_edge(
                        n, Node(p, direction.clockwise()), weight=Weight.ROTATE
                    )
                    graph.add_edge(
                        n,
                        Node(p, direction.counter_clockwise()),
                        weight=Weight.ROTATE,
                    )
                    adjacent_position = p + direction.to_v2()
                    if (
                        grid.is_inbounds(adjacent_position)
                        and grid.at(adjacent_position) != "#"
                    ):
                        graph.add_edge(
                            n, Node(adjacent_position, direction), weight=Weight.MOVE
                        )
    return graph


def heuristic(s: Node, e: Node) -> int:
    return abs(s.p.x - e.p.x) + abs(s.p.y - e.p.y)


def part_1(grid: Grid) -> float:
    start_p = grid.find("S")[0]
    end_p = grid.find("E")[0]

    start_node = Node(p=start_p, direction=DirectionEnum.EAST)
    graph = parse_graph(grid)

    min_length = math.inf
    for direction in DirectionEnum:
        end_node = Node(p=end_p, direction=direction)
        length = nx.astar_path_length(graph, start_node, end_node, heuristic)
        min_length = min(min_length, length)
    return min_length


def run_part_2(grid: Grid) -> int:
    start_p = grid.find("S")[0]
    end_p = grid.find("E")[0]

    start_node = Node(p=start_p, direction=DirectionEnum.EAST)
    graph = parse_graph(grid)

    min_length = math.inf
    min_paths = []
    for direction in DirectionEnum:
        end_node = Node(p=end_p, direction=direction)
        length = nx.astar_path_length(graph, start_node, end_node, heuristic)
        if length <= min_length:
            min_paths = list(
                nx.all_shortest_paths(graph, start_node, end_node, weight="weight")
            )
            min_length = length
    node_set = set()
    for path in min_paths:
        node_set |= set([v.p for v in path])
    return len(node_set)


def test_grid_1():
    grid = Grid(
        [
            "###############",
            "#.......#....E#",
            "#.#.###.#.###.#",
            "#.....#.#...#.#",
            "#.###.#####.#.#",
            "#.#.#.......#.#",
            "#.#.#####.###.#",
            "#...........#.#",
            "###.#.#####.#.#",
            "#...#.....#.#.#",
            "#.#.#.###.#.#.#",
            "#.....#...#.#.#",
            "#.###.#.#.#.#.#",
            "#S..#.....#...#",
            "###############",
        ]
    )
    assert part_1(grid) == 7036


def test_grid_2():
    grid = Grid(
        [
            "#################",
            "#...#...#...#..E#",
            "#.#.#.#.#.#.#.#.#",
            "#.#.#.#...#...#.#",
            "#.#.#.#.###.#.#.#",
            "#...#.#.#.....#.#",
            "#.#.#.#.#.#####.#",
            "#.#...#.#.#.....#",
            "#.#.#####.#.###.#",
            "#.#.#.......#...#",
            "#.#.###.#####.###",
            "#.#.#...#.....#.#",
            "#.#.#.#####.###.#",
            "#.#.#.........#.#",
            "#.#.#.#########.#",
            "#S#.............#",
            "#################",
        ]
    )
    assert part_1(grid) == 11048


def run_real_grid():
    grid = read_grid("data/day16.txt")
    print(part_1(grid))
    print(run_part_2(grid))


# test_grid_1()
# test_grid_2()
run_real_grid()
