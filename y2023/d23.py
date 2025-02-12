"""
We are trying to find max distance between 1 position and another.
Each position has valid next steps. There can be no cycles.
"""

from dataclasses import dataclass
from typing import Tuple
from grid import V2, DirectionEnum, GridV2, read_grid_v2
import copy

from utils import arg_first


def find_max_distance(start_p: V2, end_p: V2, map: GridV2[str]) -> int:
    max_dist = -1
    path_queues = [[start_p]]

    while len(path_queues) > 0:
        path = path_queues.pop()
        curr_p = path[-1]
        if curr_p == end_p:
            max_dist = max(len(path) - 1, max_dist)
        else:
            dps = {
                ">": [V2(0, 1)],
                "<": [V2(0, -1)],
                "^": [V2(-1, 0)],
                "v": [V2(1, 0)],
                ".": [V2(0, 1), V2(0, -1), V2(1, 0), V2(-1, 0)],
            }[map.at(curr_p)]
            dps = [V2(0, 1), V2(0, -1), V2(1, 0), V2(-1, 0)]
            for dp in dps:
                next_p = curr_p + dp
                if (
                    map.is_inbounds(next_p)
                    and map.at(next_p) != "#"
                    and next_p not in path
                ):
                    path_queues.append(copy.copy(path) + [next_p])

    return max_dist


@dataclass
class ProblemInput:
    map: GridV2[str]
    start_p: V2
    end_p: V2


def parse_file(fname) -> ProblemInput:
    map = read_grid_v2(fname)
    start_p = V2(0, arg_first(map[0], lambda x: x == "."))
    end_p = V2(len(map) - 1, arg_first(map[-1], lambda x: x == "."))
    return ProblemInput(map, start_p, end_p)


if __name__ == "__main__":
    problem = parse_file("./y2023/data/d23_small.txt")
    assert find_max_distance(problem.start_p, problem.end_p, problem.map) == 94

    problem = parse_file("./y2023/data/d23.txt")
    find_max_distance(problem.start_p, problem.end_p, problem.map)
