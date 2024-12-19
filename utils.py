from dataclasses import dataclass


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


class Direction:
    DOWN = V2(1, 0)
    UP = V2(-1, 0)
    LEFT = V2(0, -1)
    RIGHT = V2(0, 1)

    ALL = [DOWN, UP, LEFT, RIGHT]


class Grid(list[str]):
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


def is_inbounds(position: V2, grid: Grid) -> bool:
    return 0 <= position.x < len(grid) and 0 <= position.y < len(grid[0])


def read_grid(fname) -> Grid:
    with open(fname) as f:
        return Grid([x.strip() for x in f])
