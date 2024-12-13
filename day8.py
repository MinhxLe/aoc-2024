from utils import V2, Grid, is_inbounds
from collections import defaultdict


def get_antinode_positions(positions: list[V2]) -> list[V2]:
    antinode_positions = []
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            p1, p2 = positions[i], positions[j]
            antinode_positions.append(p1 + (p1 - p2))
            antinode_positions.append(p2 + (p2 - p1))
            pass
    return antinode_positions


def get_line_positions(
    start_position: V2,
    direction: V2,
    grid: Grid,
) -> set[V2]:
    assert is_inbounds(start_position, grid)
    positions = set()
    position = start_position
    while is_inbounds(position, grid):
        positions.add(position)
        position += direction
    return positions


def get_all_antinode_positions(grid: Grid) -> set[V2]:
    frequency_positions = defaultdict(list)
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell != ".":
                frequency_positions[cell].append(V2(i, j))

    all_antinode_positions = set()
    for _, positions in frequency_positions.items():
        antinode_positions = get_antinode_positions(positions)
        all_antinode_positions |= {
            x for x in antinode_positions if is_inbounds(x, grid)
        }
    return all_antinode_positions


def get_all_antinode_positions_v2(grid: Grid) -> set[V2]:
    frequency_positions = defaultdict(list)
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell != ".":
                frequency_positions[cell].append(V2(i, j))

    all_antinode_positions = set()
    for _, positions in frequency_positions.items():
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                p1, p2 = positions[i], positions[j]
                all_antinode_positions |= get_line_positions(p1, p1 - p2, grid)
                all_antinode_positions |= get_line_positions(p1, p2 - p1, grid)
    return all_antinode_positions


test_grid = [
    "............",
    "........0...",
    ".....0......",
    ".......0....",
    "....0.......",
    "......A.....",
    "............",
    "............",
    "........A...",
    ".........A..",
    "............",
    "............",
]
with open("data/day8.txt") as f:
    grid = [line.strip() for line in f]

# print(len(get_all_antinode_positions(grid)))
print(len(get_all_antinode_positions_v2(grid)))
