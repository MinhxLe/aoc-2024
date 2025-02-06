from dataclasses import dataclass
from grid import V2, DirectionEnum, GridV2, read_grid_v2
import heapq


@dataclass
class Node:
    p: V2
    dir: DirectionEnum
    n_steps: int
    dist: int

    def __lt__(self, that):
        return self.dist < that.dist


def min_dist(grid: GridV2[int], max_steps: int = 3) -> int:
    start = V2(0, 0)
    end = V2(grid.width - 1, grid.height - 1)
    node_heap = [
        Node(start, DirectionEnum.SOUTH, 0, 0),
        Node(start, DirectionEnum.EAST, 0, 0),
    ]
    visited = {(start, DirectionEnum.SOUTH, 1), (start, DirectionEnum.EAST, 1)}
    while True:
        node = heapq.heappop(node_heap)
        if node.p == end:
            return node.dist
        for dir, n_steps in [
            (node.dir, node.n_steps + 1),
            (node.dir.clockwise(), 1),
            (node.dir.counter_clockwise(), 1),
        ]:
            new_p = node.p + dir.to_v2()
            if (
                grid.is_inbounds(new_p)
                and n_steps <= max_steps
                and (new_p, dir, n_steps) not in visited
            ):
                heapq.heappush(
                    node_heap, Node(new_p, dir, n_steps, node.dist + grid.at(new_p))
                )
                visited.add((new_p, dir, n_steps))


def min_dist_v2(grid: GridV2[int], min_steps: int = 4, max_steps: int = 10) -> int:
    start = V2(0, 0)
    end = V2(grid.width - 1, grid.height - 1)
    node_heap = [
        Node(start, DirectionEnum.SOUTH, 0, 0),
        Node(start, DirectionEnum.EAST, 0, 0),
    ]
    visited = {(start, DirectionEnum.SOUTH, 1), (start, DirectionEnum.EAST, 1)}
    while True:
        node = heapq.heappop(node_heap)
        if node.p == end:
            return node.dist
        if node.n_steps >= min_steps:
            for dir in [node.dir.clockwise(), node.dir.counter_clockwise()]:
                n_steps = 1
                new_p = node.p + dir.to_v2()
                if grid.is_inbounds(new_p) and (new_p, dir, n_steps) not in visited:
                    heapq.heappush(
                        node_heap, Node(new_p, dir, n_steps, node.dist + grid.at(new_p))
                    )
                    visited.add((new_p, dir, n_steps))
        if node.n_steps < max_steps:
            dir, n_steps = node.dir, node.n_steps + 1
            new_p = node.p + dir.to_v2()
            if grid.is_inbounds(new_p) and (new_p, dir, n_steps) not in visited:
                heapq.heappush(
                    node_heap, Node(new_p, dir, n_steps, node.dist + grid.at(new_p))
                )
                visited.add((new_p, dir, n_steps))


if __name__ == "__main__":
    test_grid = read_grid_v2("./y2023/data/d17_small.txt", lambda c: int(c))
    test_grid2 = read_grid_v2("./y2023/data/d17_small_2.txt", lambda c: int(c))
    grid = read_grid_v2("./y2023/data/d17.txt", lambda c: int(c))
