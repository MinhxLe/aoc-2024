from dataclasses import dataclass
from typing import List


Grid = List[str]


@dataclass(frozen=True)
class V2:
    x: int
    y: int

    def __add__(self, that: "V2") -> "V2":
        return V2(self.x + that.x, self.y + that.y)

    def __sub__(self, that: "V2") -> "V2":
        return V2(self.x - that.x, self.y - that.y)

    def __neg__(self) -> "V2":
        return V2(-self.x, -self.y)


class Direction:
    DOWN = V2(1, 0)
    UP = V2(-1, 0)
    LEFT = V2(0, -1)
    RIGHT = V2(0, 1)


def is_inbounds(position: V2, grid: Grid) -> bool:
    return 0 <= position.x < len(grid) and 0 <= position.y < len(grid[1])
