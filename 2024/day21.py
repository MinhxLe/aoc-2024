from enum import StrEnum
from utils import V2
import abc
import attrs


class KeyStroke(StrEnum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"
    A = "A"


@attrs.define
class Keypad(abc.ABC):
    grid: list[str]
    coords: dict[str, V2] = attrs.field(init=False)
    p: V2 = attrs.field(init=False)

    def __attrs_post_init__(self):
        self.coords = dict()
        for i, row in enumerate(self.grid):
            for j, c in enumerate(row):
                if c != " ":
                    self.coords[self.grid[i][j]] = V2(i, j)
        self.p = self.coords["A"]

    @abc.abstractmethod
    def _calculate_move_instruction(self, start: V2, end: V2) -> list[KeyStroke]:
        x_keystroke = KeyStroke.RIGHT if start.y <= end.y else KeyStroke.LEFT
        y_keystroke = KeyStroke.DOWN if start.x <= end.x else KeyStroke.UP
        dx = abs(start.x - end.x)
        dy = abs(start.y - end.y)

        # calculate sequence of keystroke to type in input code from current position
        # for numeric keyboard, we bias left before down
        # and up before right to avoid the gapin bottom left.
        if start.y <= end.y:
            return [y_keystroke for _ in range(dy)] + [x_keystroke for _ in range(dx)]
        else:
            return [x_keystroke for _ in range(dx)] + [y_keystroke for _ in range(dy)]

    def calculate_instruction(self, code: str) -> str:
        p = self.p
        instructions = []
        for c in code:
            next_p = self.coords[c]
            instructions.extend(self._calculate_move_instruction(p, next_p))
            instructions.append(KeyStroke.A)
            p = next_p
        return "".join(instructions)

    def apply_code(self, code: str) -> str:
        instructions = self.calculate_instruction(code)
        self.p = self.coords[code[-1]]
        return instructions


@attrs.define
class NumericKeypad(Keypad):
    grid: list[str] = attrs.field(
        init=False,
        default=[
            "789",
            "456",
            "123",
            " 0A",
        ],
    )

    def _calculate_move_instruction(self, start: V2, end: V2) -> list[KeyStroke]:
        x_keystroke = KeyStroke.RIGHT if start.y <= end.y else KeyStroke.LEFT
        y_keystroke = KeyStroke.DOWN if start.x <= end.x else KeyStroke.UP
        dx = abs(start.x - end.x)
        dy = abs(start.y - end.y)

        if start.x <= end.x:
            return [y_keystroke for _ in range(dy)] + [x_keystroke for _ in range(dx)]
        else:
            return [x_keystroke for _ in range(dx)] + [y_keystroke for _ in range(dy)]


@attrs.define
class DirectionalKeypad(Keypad):
    grid: list[str] = attrs.field(
        init=False,
        default=[
            " ^A",
            "<v>",
        ],
    )

    def _calculate_move_instruction(self, start: V2, end: V2) -> list[KeyStroke]:
        x_keystroke = KeyStroke.RIGHT if start.y <= end.y else KeyStroke.LEFT
        y_keystroke = KeyStroke.DOWN if start.x <= end.x else KeyStroke.UP
        dx = abs(start.x - end.x)
        dy = abs(start.y - end.y)

        if start.x <= end.x:
            return [x_keystroke for _ in range(dx)] + [y_keystroke for _ in range(dy)]
        else:
            return [y_keystroke for _ in range(dy)] + [x_keystroke for _ in range(dx)]


def part1(codes: list[str]):
    keyboards = [
        NumericKeypad(),
        DirectionalKeypad(),
        DirectionalKeypad(),
        DirectionalKeypad(),
    ]
    p_keystrokes = ""
    for code in codes:
        for keyboard in keyboards:
            code = keyboard.apply_code(code)
        p_keystrokes += code
    return p_keystrokes
