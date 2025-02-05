from utils import V2, Direction, Grid
from collections import deque

MARKER = "x"
GRID_SIZE = 71


def find_min_dist(maze: Grid, start: V2, end: V2) -> int:
    queue = deque([(start, 0)])
    maze.update(start, MARKER)
    while len(queue) > 0:
        (p, dist) = queue.popleft()
        if p == end:
            return dist
        for direction in Direction.ALL:
            new_p = p + direction
            if maze.is_inbounds(new_p) and maze.at(new_p) == ".":
                maze.update(new_p, MARKER)
                queue.append((new_p, dist + 1))
    return -1


all_blocked_ps = []
with open("./data/day18.txt") as f:
    for i, line in enumerate(f):
        x, y = line.split(",")
        all_blocked_ps.append(V2(int(x), int(y)))


def create_grid(blocked_ps):
    grid = Grid("." * GRID_SIZE for _ in range(GRID_SIZE))
    for p in blocked_ps:
        grid.update(p, "#")
    return grid


print(find_min_dist(create_grid(all_blocked_ps[:1024]), V2(0, 0), V2(70, 70)))
for n in range(1024, len(all_blocked_ps)):
    if find_min_dist(create_grid(all_blocked_ps[:n]), V2(0, 0), V2(70, 70)) == -1:
        print(all_blocked_ps[n - 1])
        break


def test_find_min_dist_simple():
    grid = Grid(
        [
            "..",
            "..",
        ]
    )
    assert find_min_dist(grid, V2(0, 0), V2(1, 1)) == 2


def test_find_min_dist_blocked():
    grid = Grid(
        [
            ".x",
            "x.",
        ]
    )
    assert find_min_dist(grid, V2(0, 0), V2(1, 1)) == -1


def test_find_min_dist_long():
    grid = Grid(
        [
            "..x",
            "x..",
            ".x.",
            "...",
        ]
    )
    assert find_min_dist(grid, V2(0, 0), V2(2, 0)) == 8


def test_find_min_dist_sample():
    grid = Grid(
        [
            "...#...",
            "..#..#.",
            "....#..",
            "...#..#",
            "..#..#.",
            ".#..#..",
            "#.#....",
        ]
    )
    assert find_min_dist(grid, V2(0, 0), V2(6, 6)) == 22
