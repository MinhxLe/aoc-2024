from collections import Counter
from utils import Grid2, Direction, V2, read_grid
from dataclasses import dataclass


@dataclass(frozen=True)
class Side:
    position: V2
    direction: V2

    def is_adjacent(self, that: "Side") -> bool:
        if self.direction != that.direction:
            return False
        position = self.position
        direction = self.direction
        if direction == Direction.UP or direction == Direction.DOWN:
            adjacent_directions = [Direction.RIGHT, Direction.LEFT]
        elif direction == Direction.RIGHT or direction == Direction.LEFT:
            adjacent_directions = [Direction.UP, Direction.DOWN]
        else:
            raise ValueError
        for adjacent_direction in adjacent_directions:
            candidate_position = position + adjacent_direction
            if candidate_position == that.position:
                return True
        return False


@dataclass
class Region:
    label: str
    positions: set[V2]
    grid: Grid2

    def get_area(self) -> int:
        return len(self.positions)

    def get_perimeter(self) -> int:
        total = 0
        grid = self.grid

        for position in self.positions:
            for direction in Direction.ALL:
                adjacent_position = position + direction
                if (
                    not grid.is_inbounds(adjacent_position)
                    or grid.at(adjacent_position) != self.label
                ):
                    total += 1
        return total

    def _get_sides(self, position: V2) -> list[Side]:
        grid = self.grid
        sides = []
        for direction in Direction.ALL:
            adjacent_position = position + direction
            if (
                not grid.is_inbounds(adjacent_position)
                or grid.at(adjacent_position) != self.label
            ):
                sides.append(Side(position, direction))
        return sides

    def get_sides(self) -> list[list[Side]]:
        merged_sides: list[list[Side]] = []
        for position in sorted(self.positions, key=lambda p: (p.x, p.y)):
            sides = self._get_sides(position)
            merged = False
            for side in sides:
                for merged_side in merged_sides:
                    # TODO make the guarantee
                    if any([s.is_adjacent(side) for s in merged_side]):
                        merged_side.append(side)
                        merged = True
                if not merged:
                    merged_sides.append([side])
                else:
                    merged = False

        return merged_sides


def get_region(position: V2, grid: Grid2) -> Region:
    label = grid.at(position)
    region = {position}
    queue = [position]
    while len(queue) > 0:
        current_position = queue.pop()
        for direction in Direction.ALL:
            next_position = current_position + direction
            if (
                grid.is_inbounds(next_position)
                and grid.at(next_position) == label
                and next_position not in region
            ):
                region.add(next_position)
                queue.append(next_position)
    return Region(label, region, grid)


def get_regions(grid: Grid2) -> list[Region]:
    visited = set()
    regions = []
    for i in range(grid.height):
        for j in range(grid.width):
            position = V2(i, j)
            if position not in visited:
                region = get_region(position, grid)
                visited |= region.positions
                regions.append(region)
    return regions


def solve_part_1(map: Grid2) -> int:
    regions = get_regions(map)
    total = 0
    for region in regions:
        total += region.get_area() * region.get_perimeter()
    return total


def solve_part_2(map: Grid2) -> int:
    regions = get_regions(map)
    total = 0
    for region in regions:
        total += region.get_area() * len(region.get_sides())
    return total


test_map = Grid2(
    [
        "RRRRIICCFF",
        "RRRRIICCCF",
        "VVRRRCCFFF",
        "VVRCCCJFFF",
        "VVVVCJJCFE",
        "VVIVCCJJEE",
        "VVIIICJJEE",
        "MIIIIIJJEE",
        "MIIISIJEEE",
        "MMMISSJEEE",
    ]
)
print(solve_part_1(test_map))

map = read_grid("data/day12.txt")

print(solve_part_2(map))
