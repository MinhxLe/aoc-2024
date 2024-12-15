from typing import Tuple
from utils import Grid, V2, is_inbounds, Direction
import string
import functools
from dataclasses import dataclass


"""
    from height i, how many ways  can you get to 9
"""


def is_valid_step(start: str, end: str) -> bool:
    if start not in string.digits or end not in string.digits:
        return False
    start_int = int(start)
    end_int = int(end)
    return end_int == start_int + 1


@dataclass(frozen=True)
class Problem:
    map: Tuple[str]

    @functools.cache
    def get_num_paths(self, position: V2) -> int:
        map = self.map
        if map[position.x][position.y] == "9":
            return 1
        if map[position.x][position.y] == ".":
            return 0
        total = 0
        for direction in [
            Direction.UP,
            Direction.DOWN,
            Direction.RIGHT,
            Direction.LEFT,
        ]:
            new_position = position + direction
            if is_inbounds(new_position, map) and is_valid_step(
                map[position.x][position.y], map[new_position.x][new_position.y]
            ):
                total += self.get_num_paths(new_position)
        return total

    @functools.cache
    def get_reachable_peaks(self, position: V2) -> set[V2]:
        map = self.map
        if map[position.x][position.y] == "9":
            return {position}
        if map[position.x][position.y] == ".":
            return set()
        all_positions = set()
        for direction in [
            Direction.UP,
            Direction.DOWN,
            Direction.RIGHT,
            Direction.LEFT,
        ]:
            new_position = position + direction
            if is_inbounds(new_position, map) and is_valid_step(
                map[position.x][position.y], map[new_position.x][new_position.y]
            ):
                all_positions |= self.get_reachable_peaks(new_position)
                pass
        return all_positions

    def get_total_num_paths(self) -> int:
        total = 0
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == "0":
                    total += len(self.get_reachable_peaks(V2(i, j)))
        return total

    def get_total_num_paths_2(self) -> int:
        total = 0
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == "0":
                    total += self.get_num_paths(V2(i, j)
        return total


TEST_MAP = (
    "89010123",
    "78121874",
    "87430965",
    "96549874",
    "45678903",
    "32019012",
    "01329801",
    "10456732",
)
with open("data/day10.txt") as f:
    MAP = tuple([x.strip() for x in f])

print(Problem(TEST_MAP).get_total_num_paths())
print(Problem(MAP).get_total_num_paths())

print(Problem(TEST_MAP).get_total_num_paths_2())
print(Problem(MAP).get_total_num_paths_2())
