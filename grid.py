from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Generic, TypeVar


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

    def __mul__(self, that) -> "V2":
        if isinstance(that, int):
            return V2(self.x * that, self.y * that)
        raise NotImplementedError

    def __rmul__(self, that) -> "V2":
        return self * that

    def __hash__(self) -> int:
        return hash(f"V2({self.x}, {self.y})")


class Direction:
    DOWN = V2(1, 0)
    UP = V2(-1, 0)
    LEFT = V2(0, -1)
    RIGHT = V2(0, 1)

    ALL = [DOWN, UP, LEFT, RIGHT]


class DirectionEnum(Enum):
    NORTH = auto()
    WEST = auto()
    EAST = auto()
    SOUTH = auto()

    def to_v2(self) -> V2:
        match self:
            case DirectionEnum.NORTH:
                return V2(0, 1)
            case DirectionEnum.SOUTH:
                return V2(0, -1)
            case DirectionEnum.EAST:
                return V2(1, 0)
            case DirectionEnum.WEST:
                return V2(-1, 0)
            case _:
                raise ValueError

    def clockwise(self) -> "DirectionEnum":
        match self:
            case DirectionEnum.NORTH:
                return DirectionEnum.EAST
            case DirectionEnum.SOUTH:
                return DirectionEnum.WEST
            case DirectionEnum.EAST:
                return DirectionEnum.SOUTH
            case DirectionEnum.WEST:
                return DirectionEnum.NORTH
            case _:
                raise ValueError

    def counter_clockwise(self) -> "DirectionEnum":
        return self.clockwise().clockwise().clockwise()


class Grid(list[str]):
    def pprint(self):
        print("\n".join(self))

    def __post_init__(self) -> None:
        assert len(self) > 0
        # TODO assert all the  str length are the same

    @property
    def height(self) -> int:
        return len(self)

    @property
    def width(self) -> int:
        return len(self[0])

    def is_inbounds(self, position: V2) -> bool:
        return 0 <= position.x < self.height and 0 <= position.y < self.width

    def at(self, position: V2) -> str:
        return self[position.x][position.y]

    def update(self, position: V2, s: str) -> None:
        assert len(s) == 1
        row = self[position.x]
        self[position.x] = row[: position.y] + s + row[position.y + 1 :]

    def find(self, target: str) -> list[V2]:
        ps = []
        for i in range(self.height):
            for j in range(self.width):
                p = V2(i, j)
                if self.at(p) == target:
                    ps.append(p)
        return ps


ElmT = TypeVar("ElmT")


class GridV2(Generic[ElmT], list[list[ElmT]]):
    def __post_init__(self) -> None:
        assert len(self) > 0
        # TODO assert all the  str length are the same

    @property
    def height(self) -> int:
        return len(self)

    @property
    def width(self) -> int:
        return len(self[0])

    def is_inbounds(self, position: V2) -> bool:
        return 0 <= position.x < self.height and 0 <= position.y < self.width

    def update(self, p: V2, s: ElmT) -> None:
        assert self.is_inbounds(p)
        self[p.x][p.y] = s

    def at(self, position: V2) -> ElmT:
        return self[position.x][position.y]

    def find(self, target: str) -> list[V2]:
        ps = []
        for i in range(self.height):
            for j in range(self.width):
                p = V2(i, j)
                if self.at(p) == target:
                    ps.append(p)
        return ps

    @classmethod
    def fill(
        cls,
        e: ElmT,
        height: int,
        width: int,
    ) -> "GridV2[ElmT]":
        return GridV2([[e for _ in range(width)] for _ in range(height)])


def is_inbounds(position: V2, grid: Grid) -> bool:
    return 0 <= position.x < len(grid) and 0 <= position.y < len(grid[0])


def read_grid(fname) -> Grid:
    with open(fname) as f:
        return Grid([x.strip() for x in f])


def read_grid_v2(fname, map_fn: Callable[[str], ElmT] = lambda c: c) -> GridV2[ElmT]:
    with open(fname) as f:
        return GridV2([[map_fn(c) for c in x.strip()] for x in f])
