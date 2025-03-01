from dataclasses import dataclass
from utils import V2, Direction, Grid2, is_inbounds

DIRECTION_MAP = {
    ">": Direction.RIGHT,
    "v": Direction.DOWN,
    "<": Direction.LEFT,
    "^": Direction.UP,
}


@dataclass
class Update:
    p: V2
    direction: V2


def apply_update(update: Update, grid: Grid2) -> bool:
    """
    returns true if an update was applied or not
    """
    p, direction = update.p, update.direction
    if not grid.is_inbounds(p):
        return True

    piece = grid.at(p)
    if piece == ".":
        return True
    elif piece == "#":
        return False
    elif piece == "O" or piece == "@":
        updated = apply_update(Update(p + direction, direction), grid)
        if updated:
            grid.update(p + direction, piece)
            if piece == "@":
                grid.update(p, ".")
        return updated
    else:
        raise NotImplementedError


def find_robot_position(grid: Grid2) -> V2:
    for i in range(grid.height):
        for j in range(grid.width):
            if grid[i][j] == "@":
                return V2(i, j)

    raise ValueError("robot not found")


def apply_robot_instructions(grid: Grid2, robot_directions: list[V2]) -> None:
    robot_position = find_robot_position(grid)
    for direction in robot_directions:
        grid_updated = apply_update(Update(robot_position, direction), grid)
        if grid_updated:
            robot_position += direction


def calculate_sum_of_box_coordinate_value(grid: Grid2) -> int:
    total = 0
    for i in range(grid.height):
        for j in range(grid.width):
            if grid[i][j] == "O":
                total += i * 100 + j
    return total


def test_part_1():
    grid = Grid2(
        [
            "##########",
            "#..O..O.O#",
            "#......O.#",
            "#.OO..O.O#",
            "#..O@..O.#",
            "#O#..O...#",
            "#O..O..O.#",
            "#.OO.O.OO#",
            "#....O...#",
            "##########",
        ]
    )
    directions = [
        DIRECTION_MAP[d]
        for d in "<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^ vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv< <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^ ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^>< ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^ >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^ <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<> ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"
        if d in DIRECTION_MAP.keys()
    ]
    apply_robot_instructions(grid, directions)
    print(calculate_sum_of_box_coordinate_value(grid))


test_part_1()
grid = Grid2(
    [
        "##################################################",
        "#..O.#.O.....O.#..O...O.O.O..O..O...O...O.....OO.#",
        "#....OO........O........O..OO.O..O...##O.O#O..OOO#",
        "#..O...O......O.O#...O.#......#O.#......O.....OO.#",
        "#O.#O....OOOO.OO....O.......O.#.O..O##...O..#..#.#",
        "#.O..O...OO......OOOO...........#OO.O..##.O.O.#..#",
        "#.......O.O.OO...#.OOO..O.O..O.OO....O...O.....OO#",
        "#O...O....O...OO#.....OO.O..O......#..#.O.OO.O...#",
        "#.O.......O.#.#..#.O.......OO..O.....O#.OO.O...OO#",
        "#OO.#..#..#...O.....O.O.............OO.OOO.O.....#",
        "##O........O..........O.O#O..O.......O.O.OO.O....#",
        "#OO...O.O...OO...OO......O...........#..O.#O.#O..#",
        "#.O..#..#...O.....O.O.......OOO..O.OO.....O.O.O.O#",
        "#.O#....O..O..O..#.......O.OO............O..O.#..#",
        "##O..#...OO..O...O..#.....O....O..O.OO....##..O.O#",
        "#.O.O...OOO...#OOO.O..O.O..O.....#..OOOO..O..O...#",
        "##..##O..#.OO.#.....O#..O.O#O.O.O.O.....#..OO..#.#",
        "#O...O.O.O##..O........O..O..........O...O.O.O.#.#",
        "#.O..OO.O.#.#.#....OO.........O..O#.OO......#..OO#",
        "##O..O.....O.OO..O.O.O#O....OOO#...#..O.O.#..OO..#",
        "#...O...#.......#....#....OOO...##.OO.O..O..O....#",
        "#OO.OO..##.O.O.OO........O.O..O....O.....OOO##.#.#",
        "##.....OO...O...OO..OOO....#.O.OO..OO.#.OO.......#",
        "#O...#.O#..#.O..O...O..O..O........OO#..O.O.O....#",
        "#..#....O.#...........O.@........#....O...OO.O.O.#",
        "#.O#.........#.O.....OO..O..O.O....OO#..#.O..O...#",
        "##.#O.O..O...O.....##O....O..#..OO..O.#.....O....#",
        "#...#...#O..O.O.OO......O.OO.#OO...O..##O.....#O.#",
        "#...........OO...O.O.#O.O.O..OOO#.##..O..O.#...###",
        "#OO.O.O.....O...O.........O.#.....O..O.O.....O..##",
        "#.O#OO#....O....O.#.OO.....O.O...O.#O..OO.......O#",
        "#...O.O...#....OO....O#.....OO...#.#....#......O.#",
        "#.....OO.........O.O.....O.O..O...#O.O...#.OO..O##",
        "#...OO.O.O........#O.O......O.O..OO.....O..O#O..##",
        "#O.O#.O.OO...OO...#...OO.##..O.OOO.....OO...OO...#",
        "#........#......OO...O.....O.#...O.........O.O..##",
        "#....OO...O#O....O#.....OO....O.....#..O##.......#",
        "#.O........#.O.O......O..#.........#...#...OO..O.#",
        "#.#...O..#.O.#..#.......OOO..O..O....#OO...O.O##.#",
        "#...#O.O.......O.#..O.##OOO....#..#O.##.O....OO..#",
        "#O.O....O.O.....#......O..#...O..#O..OO#.O.....#.#",
        "#O..O...OO...#...O...O.O.....#...OO.OO....#...O..#",
        "#.....#........OO..#...O.......OO.O..O.OOO#O.....#",
        "#.O#...#O...O........O#O..O.O.OO.O..O.#..O.O.OO.##",
        "##.#..#.....O..OO....O...#.O.....OO....O.#...OOO.#",
        "#....#O.#.....O....O..O.............O.O.O#.O...OO#",
        "#.OO.......O..#.O...O......O#.O..O.#.#O.#.#.O.#.O#",
        "#.......O.O...O..O......O..O.OO.....O...#..O.....#",
        "#........O#.O.O......O#.O.#..O##OO.O...O...O.....#",
        "##################################################",
    ]
)

directions = """
<v^>><vv>>><vvv<vv^^v>><^^vv>>^^^>>v<<v><><>^<<^vv>>>>^^^v>v>^>^><^v^>^^>v<<^<v>v^v<v^<>><^<<v<^^<^vv<^<^>>v><><<<>><>><<^<<^v^^><><<v><<^vv<<>><>^>^^>>>>^^v^^vv^v^>^<><>vv>v<v^<<^>v<><^>^v>^><>>v^<^^>>vv^><v<^v^>>v^>><v<v>^vv><vv<vv<<v><>vv<<^^<>>>>>vv<v>vv>^^<>v>v^v^>v<^<><>>^^><<v>v<>v<>vv^v>vv<>>vv<<<<>v^vv^<>^v^^^^>^>v>>^^v><<>v><<><^><>>v<><v^>^>><^<v<^>v^><^>^<v<^<>^^^v<^v<^^<<vvvv<>^v<>>v<v<^<vvv<<v<vv>><<<<v<v>^>v<<<^>>^><^^><>^^>v^v<^>vv<>><<>vvv>^^<<v>^<^<><^^<^v^>><v>v>v^><v^<<vv^^>vv>v^<>v>^<>^vv<v<>^v<>^^^>>v>^><><>>><>v^><<vvvv^>vv^>>v>v<<<^^^<^><vvv<<vvv<><^<<<^>>v<<<><<v><v<><<^^v^v^v><>v^<v^^<^^^<v<v<<v>>>><v^>^>v<>><^>^<^><^<><v^><vv^v<>v<<v>v<vv>vvv<><<^^^>v<<v^v^^vvv^<^v^>vvvv>^^<<><<<>><<^v<>><vv<>^^^<<>>>v><^v<vv<<^<^^><^<^>v>v^^>^><^^<>^<v<v<<v>>><^>v><<<v<v^v^^v>v^>^<v><vvv<>>^><<v>vv^v^v^>vvv><<>><<^v<<v^^^^><^><<<^v<^vvv><^^<^<v>^^<<^<^><><>>v>>v>vvv<<v^>>>^^v^v<v^^v><^v^<^>><v^<<^^<<v><>^>^<v><>><<<vvv^>^>><<^vvvv<vv^^v<<>v<><^><^>^>vv<>><v<vv<>v<<^<^><>^v<^
v^^<<v>><^^><^>><v^>><^><>><v>^v^v^v^<<<v<>^<^<^^^<><<>>^<v>>vv<>>^<>^<vvv<v^>><v^<><^^<v><v^<>>^>vv>^<^v>v>^<v><<^^v>v>^^v>v>^>><<<^>>>v^vv^>^vv>^v<>v^<<>>><<^<>^^^<>^<^>^^>><<v^v><v<<>>vv^v<>^<<>><>>^^^<^^v>>^^<v<>v>vv><v^<^<vvvv>^>^<<>>><><^<v^^^^>v>^>><v>>^^<vv>^<<v><^^^^>^v>>vv^>>v>>v<<<>v<>><v<v^^>>^>vv<>><v^><><<>>v^><vvvv^<vv<v<v>^>^^><<v<v^^vv>v^v>v>v>v>><^<vv>v<v^<v^v<v>>^v<^<<<<>><^>>>v>>^>^^vv<><<vvvv>^v>v><v^<<v<>>>v^<<><^>vv^<>v^^^<v<^><^^<><<<<^>>v>>^>>^^^^^v^<<v^v<>^^>^>vv>^>v><vv^^<^^>^<v^<<^vvvvv>^^v>^<^<<v>>><^><vv><>v><^>v^>v^^<>>>>v^<>v^^>^v<vv<v>v>v^><>vvv^v^<^^v<vv<^<<v>>>v>v<v><v<vvv^<<><>><v<<v^<^<^>>v^^<><<<^v<><v>^^>vv<<^><^>v>^>^^v^v<>^^<^v<^v<<<^<<v>>^>vv>^<^><v^^v<^^<<<v<>v><>^^>^<><>^v<v>^v><>v>^>^v>v<<v<^<<>>v^<<^vv^^^v^><<vvv^^vv>^^^^>>><>v><>v>><^>^<<v<^<^<<^v>^v<^vvvv<v><<<v>><<^>>v^^^<<><^vv>v<^<<^<vv^^^<v^v<^^<^v>^v^^v<^<vv>>><^<v^^<<vvv><<>^>^><><>^v<<<v^>v^^>^<>>^^<^>>>^<>^<^^v^>^v<<vv<^v>><><>v^vvv^v^>><<^vv<^^v>>>>>><>><vv<^vv^vv><v<<><v<<>>>>>^
^<^v^<<>>><v<v^<>^<v^>vvv^>^<^<>>>>^^^<<<<<<>>><<>>v^>v^v>v^^<v<><^<v^><^>^>v>^>^^>>>^^<>>^<^v^<>v<^v><v<<v<><^>>^v<^^><^>vv><vvv>><<>><<<>vv>>vv^>vv<^v^>>^<v>v^>^<<<v^>v><<v><v^<^^v<<<^<^<v<^<v<v<v<>v>^^v<v^<><v^v^v><^^v><v<>>^><>v^>v>v<><vv^>v^>^v<><vv<>^>>^<v<^>^>v<>>v>^v>^^^v>vvv^>v^^>>><<><<vvv><<v<<>^v<<v^>v<>vv^v<>^<>v>^vv>>v><^^<<vv><><<v>^^^>^vv>>>>><vv>^>^<<>v<^v^<>><v^v^<v>v>>^v<v<<^v<vv>^vv^v^^v<v>vv<>vv^^<vv<><^>>>>>v^<^v^^^>v^vvv<^v<v><>><v<>^^v<^^v<^>>^vv^>v<^<>>^v>>>v^<<v^v^^>v><v<>^^<>vvv><vvv>>><>^>v^<><<v^v^v><<^^v>><>v>><><<<<><<^<<<>><^^v^^vv<<^^><>^v><v>^^^vv<<><<^><><<>v>>^<v^v>v>^^vv^<><v><^v<<<<^<v<v^v<^<>v>^v<<^>>vv>^v<<<>v>vv>v^>vvvv><>v>v><><v^v>v^>>^>^v>^>^<vv<<v^vvv^>vvv^<^>^>>v>^<<>^v<v^<vv^<v<<vv<>>^^<>vv^<vv^<v<^<^<<>v>v>^v<<vv<>v<<^<^>v^>^><vv<<>>^<<^v><<^<v^^^>^^>v^v>^<^^<^<>^<<v>><v<<<<><v^v^>>^>v>v<^v^^^vv^^<vvv^<^<^><vvvvv<<<<v>><v^^<^<><>>^<^v^<v>>vv><<v^><^<<>vv<^><^vv^^v<><^>^^v<^>v>>vv^^v>^<>v^>^v<vv^vv>v>^^v<^<<<>^vv^v<<vv^v<>^^><vvv^<^>^v>^^>
v>vv>><>v^vv^<<><<><<^><<>>^v^<vvv>>v<><>vv<^v<<^v^v^<>^vv<v^^<><>^<v<<>^<<^<v<^^<>>^v<v<>^v<^>vv<vv^>v^vv<v^<<vv<^>>^<><><<vv<^>>^v^^^<^v>^<<>^<>><^v^^^>>v>vv>v^^v>>>v<>^>v^v^><<^^<>^v>><^^>vvvvv<v>^v>v><v>^<<>^>v>v<v>v<v^><>v<v>^>v<>>^^v>vv>^^<v^^<>^v>^>vv<^^><<vv^v>v^<<<>>>^><^^^^^v<>v^<<^v^>^>>vv^><v<^>vvv<v>>>^v<v><^v<>vvv>v^>^v^>v^<>v>v^>^<v<>>v>>>>^>>v<<v<^>^vv><<>>v^v^^v>^^vv>>v>^>>>vv>^><vv>^v>>v^>><^^^>>^vv<v>>vv<<<v<^>>>^><>vv<>><>v><vv><<^^v<^vv^>vv><<>^>>vv>>^^v^<v<<^<>>v>^<<<><^^<^<v<<<<^<v<^>v><<^^>vvv<><^v>><vv<<>>v<<><<<v>^>>>>>>^<^><^^>^v<v>^v^^^>v<<>^v>^>v<v>^^^><>v<v>vv^^^^vvv<<^<<<^><^><>v<>>>^vv<>v>^>^^>^vv<^v^^<>>^>^v>^v<v^<^vv^vv>>v^><^<vv>>>v^^>^<<>>>^>><>^v<<^^vv><v<<<>>^^<^v^>^><^><v^^<>>>vv>v^v>^<<<>v<^^^<<v<<>>>>^v<v^^<^^vvv><v<^>^v>><vv>^vv>^<^v>^<>^v<^^>^^^vv<>^>>>>><^>^<>^^<><<v<^^>>^>vv<vvv>>>^><<v<^>^<>v^>v>vv^>^>^^>v>>>>^<v>>^<><vv>^<v<>^^<>>v^<^<v><><>v>^^vvv^v>>>vv^><^v><^>vv<vv^<^<vv^<>>vv><^^><vv<vv<vv<>v>v^>^v<<><>^vv>v><>^^v^^<>^v^>>^^<v<<^v^>>^
><>^^v^>v><^<^v^<v>^v><<^<<<v>^^v><^<<vv^v<<<>v<^^<^>>><^v>v<vv^vv<>^><>vv>><><^^^><vv>v^>>vvv^^>v<v^<><vv^<>>><v<>v>>>^v^^<>^>><v^v^><v<<v<<v^^>>^<<<^^vv^^<><<>v><^>>v^^>^<<>>^v>v^>><<v^<^^<v<><vv>v<<v^vv>^<vv<<>>>>><v^^<<<v>>v><v<v<^>>^^^^v^>^^vvv>^>><<>^<<^v^<>><><>v<v^^>><^^<v<v^^<<>v>><^^>v>>vvv<><^v^^><<^<v<^v>v^v>^v^>>><^<^>v<<<^vv>v<^<^^<>v<v^vv<>>^>>v^^v<v>v<>><>><^<><v^><v<><>>v^v^<<v><v^<^>v^<^v<v<v>v>>^<^^vv>^<^^^v<><<^^v<<<^^^v>>><^vvv^v>>^>^^^<^^><^<^^vv><v^<<>^vvv<v^><v>v^>v<^^^>^>><v^v^^vvvv>^v<v>>^>>^^^>v>vv^<^^v<^><><><^^vvvv<>vv<^>>>^<v<>><><v>>>>>><>><vv^><^>>>^^>^^^><^>vv<v>vv^^<v>v^<<><^v>v<<v^<>^<<^<<>>^<^v>v>^^v<^<vv^vv><><<^>^^^^v^<v>>v^v><>><v<^^^^><>^^v><v^vvv<<>^>>><v^><vv>vv><^<>^<^>^>vv^<v<<^>>^^v>v<<>v^^><>>v>^^^>^^^v<>>^v>v^^vv>v<^vv><^><v<<v<<v<v>v<<>v^<>vv>><<<^><>>v<<>^v>^vv<>>>v<v<^vvv>>^^<^v<^v>^>v^^<<^<<>^>^<v^><>>vv<<^>v>^<^^>^v<^>^^v>>><<v<>^vv>>v>v>v>^<>^>^v<^^v<^>^v<<<><^<v<^^<v>^v^^v>^^<v<v<^^<v<<vv<>v>^vv>vv^v<>v>^>>^>^>>><<><v<v>>v<>v^<vv<>v
>>^>vv<vvv^<vv<<^^v>^<>v<v<^<<>^>v>^<<<^^<<<^^>^>><^^v<<<^<^<>><^v^<>^v^<>^^<^>><<^<<<<<><^>v>><<^<^<v<^><<>vv><<>>><v<vv^>v^<>v><>vv^v>><<v^^<<>vvv^v>vv<<<>^<<<<<>vv<v^^>^>v><v><>>v^v^<>v^>>^><<^<^><^<^<^<>>^^>>^^^>v<<<^<>vvvv>v^^<>v^>>vvv<<^>vv^<^^<v>>>^v^v^v^^v^v^>>^<>^>><>>>v<^>>>^>>><v^v<^v<vv><<^>>v^v<>^<>>^^><v^>vv<v^vv>v^^<<^><^>>^^<^v><v^v<>v><^<v^^^^^vv>>v^>>>>>^vv<^vvvv>>>^^v>^<>^v^^>^<<>^v>>>^>>v>^^v<^^>^^><^v>>^^>^>^^<^<><^<<^>>^>^^>v><^>vv^vv^><<^<^>v>^v<>v^^<<<<v^^^<>^^<>^^^>^v<<<vvv>><vv<>v^^<<^^><><vv^>><^v>><^<^><>vv<<>v^>vv^v<><<^>v>^><^<><v^>v<<v<v^v<v>>^v^>^vv<^^^>^<v><<vv^<v<^v><<v>>>vv<^<<>v>><^>>><<<^>^v<>>v<^v^<<^>><^>vv^>^>><>^^^v^><^vv<v^>vv><^v<>^<<v^v><<^v<<^>><<<v^><<v^>v^>>^>>>v<v<v^^<^^^><>v>^^v<<vv><>v^^^>>^<^>^v^^v<v^^^^>v>>>vv<<^><^><<vv<<v<>>>v>>v>^>>>><^v^^><v<^><<<v>>^^v<vv^v<<<^v^><>v>>v><^^v^<>^><v^>^^>^v>^v>^^v<^<<<<>^v>^><>v>>^^v^vv>>>^<^<v><^v<vv<vv^v<<>v^v<<v><v^<>>v>vvvvvv^v^^v<<>^<v>>v>v>><><<v<><<v^<>^>v^>vv^^v>^v^^^<v^<<<>>v^<vv>^v><^v^^^
v>^v^>v^v^<^>>^v>v<vv>><<v>>><<>^<^<v<>^v^^>v<^v<>^^<^v>^v<^<^^<<<<<<v><<^>v>vv^v<>><>>>^>^<<>v^<<<>>^^<v<><v<>><^><v<><vvv>v^><^<><>^^<>v^^>v>v>v<>vv>^^<<v^>vv>vvv<<<>>^>^>^v<<><v>^>v>>><^vvvvv<<^^v<>^v^>>>^>v^>vvv^v^v><^<>>><v>>v>v>^v<v>^^>>^v<<vv<>^<^^v^^>>v^>^<<<^<><>^<<v>^v^>>><<v<>>^<vvv^^<^v^^^>v<>>>v<^><^^^^v^<^^^v^^><><v>>>^v<<v<vvv>^>v<>^vvv^^<<><v<^<<>v<>v^<>vv<<^v^^^v^vvv^v>^<<<>v^<^<vv<^<>><^v^<^^^^^vv^v>^<<<^>><<v<v>>^<^^<<>v<^<v>v^v><><<v>>vv<<^<v<^^<v><^<^^>>>>>^vv^<^v<<<v^<v<^>^vv><^v^v<^^<<<v^^vv>^<^<^v^><v<^^>^<>v>>v^^^^<v>v^<>^v^<^^^>>v^^v^<>vv<<vv^<<>v>v<>v^>>><^^>^>>>v^<^v<<<v^>^>vv>^>><<<<<^>v^<<<<<>v<><^^vv>^^<^vv><>^>><>v<<<^v><^>^>>>><>v^v>>>^^<<v>><v>^><^>>>vv^^v>v>^<>>>>^<v>v><^^<v<>^>^<<><<^^v>v>v>^<^><^v<vv<>^v>>^><>^>v>^>v^<v<v>v<>>^^>v^><vv^<^v^v>v<vv^v<<v^<<^>>^<<vv>>v^^^^>v^<>v<<v^^v<^<<<><<v^<>^^^>>^v<>^<><<v^^^^v>^^><^^^<<^^>>v>^v>>^<<>^<^>^><>v<>^>^<^^>^<<<^>>>v^<v>>^v^>v>^vvv>vv<^v>^><<^<^>><<v^><>^>v<<<<^vv>><><>^>><^>v^v<^v>><>vv<vv>v<>v>>^><<>>^
^>v<<<<<><v<^>v<>vv^>>^<v^^>vv^v<v^>v<>^v^v^^^>v>><v^>><>>^v<<>>v^<<^^>^>^<>>v^<^>v>^^>><>><<>><<<<^>>v<v>><v<>>>>>^<v<<v^<vvv^<<<<><^>v<<vv^<v<<^v<^><^^v^vv<><<<v^^<^<vv>^>><><>v><>v<^v<<^vv<^>><><^>><<<vv^<><v^>><v>v>v^>>v^>vv^^^^v<^vv^>vv>>>v>^<<<<><<>v>vv<^^>vv<>><<^^vvv^^<<^<<<>v>>^<>^<v<^>^^>v<>^^^^^>>^^v^<>^<vv^v<<v<v^^<><v><v^<><<<^^>><v>^^^><<><><v^><>^v<v^v^<v^>v<v>^<<^>^>>>^><>v>^<v<v<vv^<v><<^^^^<^<<v<>><<<v^>^^<^<><<^v^v<v><^>^<>>^<v>^><^<<^<^^^<><<^>^>v^vv>v<v^>^<<^^v><>>>^>>^v<<<^^^^v^^><v^>v>v<v<<v><^>v><v><v^<<<<v^^^v^^vvv^<v<<vv<^v><<v>><^^>v>v>^v>^^<>vvv<^>>><>>>v^>><v>>>><v<<<^^v>^v^><<<v^<>v^>v<>^^^^^<^<<v^^^><vv>>^<><vv^v<><^>^vv^>^<v>^><><>v>>v>^^><^<>v>>><>^v>v<>v>>^^^v><<v^<><>^v^^>^<><^v^v<><<><^<vv<vv>>v^v<>>^<^><vv>v^^^^><<<vv^^>vv<v^><><^^<<>>v^vv^v<vv<^><v>>v>^<<>v^v<>>><>vv<^<<><<<>v<><^<<<^>^<^<v^<^v>^^<<vv^>>>^v<>>><^><<^^>>v^vv<^v<v>vv<>>v<<^v<^v^v^^>v^^^<<^<<<^v>>v><<v^<>>v<v<v^>v>>v<<^v^>v<>><^^v><^^>^><vv<^^v>^><v^>^<>><<v<<>><>v^v^^v>>v>v^<v^^^v<<>
^<<v^>^v<>v>>^^^<v<>>^><^^>>>>v><v>>>^v<^v<<vv><^>^<vvv<vv^<^^v<v^>><>>^<^^^>v^<^^>vv^<>^<<v<v^^>>^>>><^<><^<^<><>>><<<<>^><vv^>>v<>^<>>vv><^>vv<<^><vv>>v^>^v^v<v<>>><^v>v><v^<>>^^><<^>>^^><v<>v^<vv>^^<>>vv^<v<>>v>vv^v<<^>vv^^vv^<><^<<>><><<vv^v<^^vv^>^>v<^^>>vv^^>vv<v<^vv^<>v<><v^<<>v>v^>v<^v^vv^v<v>vv<>vvv>>^<^>v<><>vvv>v><^>v<>^<^^v^v>^>v>^^>>v>^<^>^^v>>^>v<>^v<v<<>^^v<^>^v>>^vvv>^^vv<<v>v>>^v^v>^v<vv<v<<><^><^<v^<^vv<v>v><vv<<><v>vv<^<^<><^v><^^^vv<>^v>>^>>^^v^vv>>^^>^>vv^<v^>v>>v><^vv>v><>>>^^>>^v><<v<><<vv^^>>^v><>vvv<v>vv^^v>v^<vv>vv^>>v^^>>^<<<<v<^^^<v^v><^<>vv>^^<v><><^v<>v><>><vv<v>^^<^>v^>v<vvv>^^<<>>v<v^<^vv<<v^>><<v>^^^v<<^v<^^<^^v^<>v>v^v<^^<<v>v^v<>^<><>^>><^^>^<vvv<^<<^<>vv^v>><<<^^v^v^<>^^>><<<>>vv^<<v<^>^<^><<>v^^>vv<vv^<v<^>v>v^^^^>^vv><>>>><<^>>^v<<><^^v^>><>>^vv>>vv<v>^<vv<>^^^<<>vv^^><v^><^>v<vvv^^>><>>^>v<vv>v^<^>v<^<>>^^>v^>v^vvv<>vv<v<^<>^>>v<<><<v<<v^>><^^<^v<<^vv^<vv>><<>v<vv^<<^vv^>^^v<>>^^>v^>v>v<^>v<v^^vv<>>v>^^><><<>v<v><v^v>v<>v<v>^<v>^vvv>^<vv<<><<<<>^^
vv<^<<><>>v^><<v<<^<>^>^>><<^v<>^v>><>vv^>^^>>v<^^>>^<^><^v>>>v^^^>v<<<>>><><>^v<<>>^^vv>^<v^^<^v<<^>v>v<v<<<>^>^^v^>>v<v><^>^>^^<v^vv^vv^v>>^v>><v>^><>>^<>>v><>v><<>^^>^>vv<^v^v<<v<^>v<<^^<<<>>v>>^>^>>vvv^vv>vv^<^v<vvv<>^>>^^^vvv><>v^<<>vv>v>^<v^^>v^v>v<^^v^^>v>^<>v><<<vv^<>>^v>>v<<<^^<v>>^<^>v>^<<<v>^^^><>><^><^>v^<^^<^>^>><<^^<>^<>^v><>><^^>v>^>^<^<^v<<vv>^>>^^<<v><>^^vv^>^^v^<>v^^>>v^>^^v^>><v><>>v<>^>>^>^^<v<<>><^>><<v<^>v<vv><<<vv>v^v<vv>><>vvv><vvv^v^v^<^<^<^<^<^<><^><^>>>>>>v<^^<<<^v>v^v<v^><^<v^^v^v^><v^^v^^v>>v<<>^v<v<v<^^<v^>^^><^^>vv>^>^>v^<<<^v>><v<>>>^>^>^^^v^<>v>^<<^<<^>v^>^^><v>^v><v>v><^>>v>^vv^^^<v>>><^^>^>>>v<v><v^v<^v^<^v^<<>^^v><^<<>v<>><<>^v<v>^^<^v><v<^vv^^><^^<>^>>^v^^>^^<>vv<><^>><<vv>^^<^>^<v^v^vv<vv>>>>v>>vv<v<v<><^v<^v^>^>>>><<vvv><vv^>^>v<vv^^>v>><<>>>^v>v<v<>^<v<^>>^<>vv<<><v^v^<><^^v^>v<^<><>v<v<>^v<^^v<^vv^>vvvv>v>>>v<>v>v>^>>^<<><<>>^vv^>^^<^v>v^><<vv<<>^v^>^v<v<^<<>vvvv<<vvv>^>v^v^^>>v<^>><v^><vv<^<vv>^>vv>^>><v^<^^^<v<>v<<><^><<^<^<>^>>v<v^<<<v><><<<<
>^^<v<>^v<v^^>^^^vv>^>>^><v<vv^^v<v>vv^^^><v^^>>v<<vv^^>v<vv^^><^^^^<^vv^>^<vvvv>>>><<>v<>v><vv<<<<>^<<<^vvvv^vvv>^<^v<>>^v><<^>>v<^vv<^vv>^^^>^^<v><><>vv><^<^>v^>^^vvv^<>>vvv>>^<<^>v<<^^<>>><<v<vv<v^><v<vv^v^v^v<v^>^>^>^^><>>vv^v^<v><v>vv<vv<<<<>>>v^^>>^<v<^v<>>v^<^<<>^^>>><vvv><^<^^<^><v<<<vv>^><<>^<^<vv<><^<<><>^<v^^^<>><^<<v<v<<<<><<<^v<<^>>v^v<<<<<^>^v>><<^^<>vvv><>^><^v^^>vv>v^<<>^v^>>v>v>^v>>^v<vv><<^^<>v>^^^>>><<<<><>^^v>vvv^<>>>^v>^^>>^vv<vvv^^>^>v^<<^^<>^<^vv^^v<v>>^>^>v^^^^vv^^<>>v><>>^<^vvv<v^<v>v<>^v>^>^^v<^>>>>v><<^^v<<v><^>v^<<<^v>v<>vv^v<<>v>>v<>>>>v>^v^^^<^>^><v>^<<v><><vv<^<<<^v<^<v^<^^>^>><v<^^>v><<<>vvv<^><v^v^^v><<<<>^^<v<^>^vvv^<^<<^v<^<<^<<v>v<v^^^v><><^><>v^^vvv<vv<vv^v^>>^><vv><vv<v>^<<v>^<^^^^vvv^^><>v<^vv><^<v^>v^<v><>>>v<<^>^<^<<<vv<<><v>>>v>^><v>v>v>vv>^<<<^^>>>v<^v<v>^><v><<^v^^^vv<>^<v><^>^^><^v><><v>>^>>v<^v>>><><^>><<v^<^>><<<<<^><<<v<v><v>^v>v<v^v>v^<^>^vv^<^v><v>><>v>^v>^<<<>v>^^<v<<>v<^<^^^^^v>^^^>vv^v><>vvv><^vv<<^vv^<<>>^><^^>^^v<^<<^>>>vv<^v^<v^^<
>>>^^v^v^v<<^>v^v^v<><<<<<v^>>vv^<<^v<v<>>v^v^<>^>>>^><^<>^vvv<>>>v^^^<v>v<<v>>v<<<v<><vv>^v<^><^^<vv><v<<^^><<v>>^v^^^v>^<>>>>^^^^>v<v^<<<<v>v^v<><v><>v^v<vv>>^>v>^><>v^><^^>^<>vvvvvv<>v^^^>v>^^v>>vv<>v^^vv><>>>>><<<^<v^<vvv<vvv<>^<v<>^<<v^^^^>^^>><v<v<<<>^^><v<vv^v>v^v<^vv^<<^^^<vv<^><>>v^^v^v^v>vvv^v^vv>><^v<^v<v<>^<>^<<>v>v^vv<vv<v<v^>><><<><<<>v><^<vv>vv^^<^vvvvv^<v>^>^>^v>vv><<^v<>><v^v^v>v><>v^>>>v^>><<v^vv>^v^<^v^>><v<><v<vv^vvv><^^<v><v><^<<vv<^<v<vvv<<vvv^<v^>>>^><v>v><^^^<^<>>^>v>v<v<<<vvv^^^<v<^><<>^<^<>>^v<vv>^>><v<^^>vv^^^^v>v^v^^<>><<<>>^vvv^v^v>>v<v<<>v<v<<<v><^^vv^v<<><^^<<<>^<^v^<<v>v<^>>v<^v>v><^>>><>^>>^vvv<<<<^>v^vvv<<<<<>>>^<^>^^^^v>^>>^>v^v^><<<^<>^>><>><^^v>v^v<v<>v^<^<^<<<v>>^^vv<<>vv>v<><>><><><>vv<>v^^>>vv<<^>^v^><<<<^^<^<v><>^>>><<>^^>v^>^v^>>^>^v^v><>v>^<v^^<>vv^^<v^v<^v<v<<^vv^^<v^<<^<<>v>vvv^><>v^>v>vv><<<v^v<<^v><^^^<>^><^>^^>v<v^>><>>>v>vvv>><><vvv>^^^v<><^v<<v>v^^>^v^^<<v^><<>vv^v<^>vv<>>^^^v<^vv<v<^<><>v>>^<><v>>^<>><<>><^>><>>v<<<>><><<>v>^<>^<<>>^^v
^^>v<^><^v>>><<<<^>>^^^<vv<>><v>^<^^v^^^v>^v<<v>^^^v<^>>^>>^^v>^<^v<>v^<>><>><>>>^>^^>v^><>^v<>^^<<v><<<^<>v<vvv>><>>v^vv<^vv^^<v>v^^^>^>>^v><v^<v<v^v<v><^v<v<^<^<<>><<v>^<v><<v^<^>><^v^<<>^>v>^^<<^>v^<>>^v^<>v>v<<^><v^<>^^^v><^^v^v>^^>v>>v<^<v><v^v^v>^^vv<v>><>v<>^^>><^v<v^>>vv>^v<^<v<vv>^^^>^v>v>v<<<vv<v>>vv<>vvv<^v^<>>^>^<>^>><<^vv<^<^^v>v^>>><<>vv>^>^^^>^>^>v^>^<v<v><vv^^>><vv<^<v<>v^v<<^^<^>>v>v<^>v>^<v<<v><v>>v>>v^^>^>><v<>vv<vv>^<<<v^>>^>v><>^v>^<<v^v>><^>vv^^^vv><^v<<^>>v^><>v^^^<v^<^<<>>v>^^>^v><v>vv^<<^<>>>v^<^^>^^<^v^>^<<v<^^<<<>v<><vv>^^><v><>>>>><^>>^><<^>><><<vv^^^>>>>^><v>>>v<>v^^<^^<<^^^vv^v<v^^^v^<^<v<<<^v^><<v>>^<^>^<v>>v>^^><^v<>vvv<>vv^vvv<>v>v<v^<^<v<><>v<<v^v<v^><vv<<vv^<v<<<vv<v<<<^v^^^>v>v>>v^^^^>^^v<>>v<v^^>^v><<>v>^^vv^<vv<^^><>^>vvv^^vv^^<v<<>^v>v>v>v<>><>^^>><^<^<v<^>^<<^v<vv^vvv>>>><>>^^<^v>>^><>vv^<<^>^^>^vv^^>>><<<^v<^<>v<<^^v^<^vv>v<^<<<^>><>^^^>^<^v>><^v^^>^v<v<^<>^><><^<<<>^<>vv^^<>><^>>>>^>>^vv^<<^>^>v<^v^v^v<^^<^^>vv<v^^^v>>>>^>^><><>>><>><><v^>v^^><
v<<^^^v^<>^><^>^^<>^v>^^^v<v<><>vv^^>v^^><<>vvv>>^<><>v^v<^v<v^<>v^>^<vvvv>v>^v<^>^^v<v^<^>>>><vv^^^<>>v>^<vv^>^>^><vvv<>>v^v^>><>>>^v<>^v^>>v^>v><^v^<><v<<v^<^><^v>v^<><>>v<<>vv>>vv>^^^<>v<v^vv><>vv<<>^>>^<>>v<>^>^<>><^^>v<>^v^v>^>^^>><v^<<<<^^v<<v<v<vv<v^v><>>v><>^vvvv<>v^vvv<<v<<<v<<v<v><^^>^<>^v>>>>^<>><<v<v<^<^>^<<<><vv<>vv<>v>v^><v^^>vvvv^><v^^^^>>>^<<>^<<^><^<^<^>><^^vv><v^<v>><>>>v<>><><^<<<>^<^^<<<v^><v>>^<>^>v<v<^>v<<<<v^>^^v<>>^<<><^vv><<^v>v^v^v^v^^v<<v^vvv^>v<^v^^vv^<<<vv>><v^<v<vvv^^^v<v>>>>v^v>^>>>>vv><>vv^>^^^vvvv>>>v<>>^><v>vv<<<>>><v>><>>>v>>v>>^>vv>^>v<^^<>vv<>v>>><<>>>^>v>>^<v^^>>vvvv<><v<v<^<v<>^^>vv<<^v^><v>v<<^<<<>^>^>vv^>v^v^<v>><><>v<>^^>v>vv^v^v>>^v^>^^>v^v^<<<^><^<^>^><v>v<>v>v>^^<^vvvv^<^^<<v^<><>^>^>v<^^vv<vvv>^v<v>v><^v^^><<^v^^^>vv>><><v<^vv^^>^<<>vvv<>v<>^^<^<vv^<v<v<v^v<v<>v^v>^<>^<^>vv>v^^v^>^>>>^>^>>vvv><<><^<^v><><>v^<^^^><v^>^^<<>^^vvvv^v<<<v^>v><>>v<>^^>^vv><<^^^^<<<<>^vvv^^^v^^^vv>>^>>^<^^<><^>v><^v<<vv<v<vv^^<<>^v<^<^vv^<><^^<<<v^>>v^v<>^v<v^^^^>
>^^<^v^>^^v<><vvvv>>^<^>^^v<^v<^>vv<<^><<^vvv^<<v<v^>^v^>^^<v^>^>>^v<v>^<<><<<<<>>vv<vv^>><>^<<^<v>^^<<>v>><v><v>>><>vv>v<<^vv<>v>v^<v^v>>v>vv<^><vvv>><vv<^v>>>><<^<^^<<>^>>^<<v^<><v<v^^>>><^<v<^<<v<><v<v<><v^>>^v<<<^<vv^^^>^>v<>^<^v>^^v<vv^<<<^<^v>^<>^<vv^vv<>^^^>^>>><v^>v<^>v<v^<^vv><^<^>><v<^>><^^>><>>>^>>v<><>v^><>v<>>v^<v>><>v<^vv^^v<^>>>v>v<<vv><>>^<>v><v>v><>^><^<vvv><^>>v>>^vv^>v>^^^<>>>v^<^^^<<>>^^v^^^<>vv^>^><>><>><>v>^^>vv<vv>>v>>^>>><<>v>>v^<vvv>v<vvv>>><vv<^vv>><vvvv<^<>>^vv<vv>>v^v>^^^<>>><^v<^^<<v<v<<v>v<>vv>^v>^<v>>^<^<^v><v>>^^>v<<vv<<<v<v<<>>>^v^^v<vv^>v<>^>v<>><>v<><<<v^^<>^^<v^^^vv^^<>><<<>^v<^>><v<v^<<^><>^<<v^<^v^v^v^<>^v^v^<>><v>^<v>^<vvv>^<>>^>v<vvv<><v^<v>vv>^^>><^<<<><<><><<<v<>><>^>v<>v^^^<^>>^>^><vv>>>>v><v>^>^<vv^<><^^<>v^vv<<<v^^v^<v>><v^^<<^>vv>v>v<^<^>^vv^>>vv^^<^^vv<>vv<><>>><><^><>>^vv<<<^><^<^<^v<^<vv>^^<>^<v>>^><^>^><<<<>v^>^^^v>^v>^v>>^<^>>v<<<><<><>^>^^^^^^<<v<>^><v^^v^^^<v^v<>^v>vv^^<v>v>^^^^v<<^<>^^^>v<^>>v^>><>>><<>^vv<<>^^v^^^^><^v^^vvv<^<<^^<>
^^<><v^<^^<v<<v<<<<>v>>^^<>v>>^>v^>^^>vv^><^vv<><^v<vv>v<>^<>v<vv>^>>v<<>>v>v<>v>><<v^<^>v^>>v>v>^>vv>^<>v>^v^v><>v><>^^>^>^^<<>>^<>>>v<^^vv><>v<<><^>><<^^^^<<vv<>>><<>vv<><<vv^<><vv<^v<v<^v^vv<v^><^>v<>v^^<v>>vv<><v^vv^<<>^<<vv^>v<>>v<<^<>vv^vv<<>^v<v>^v<^<<><^>v>>>><><vvv<>><>^<v>v^vv^<<<^<><v>vv^>^vvv>vv><<<^^^<>^^<<^<^<><v>^<<>^^<<v<v><<^v^<<>><<v<vv>v^<^v^^<^^>^<>v^>vvv<v<><<vvv^^>^<>v>^^v><<v><vv>v><vvvv<<>^v^^<v^v<^><>><^>>^><^vv><>vvvv>v^vv<^>v><<<^vv>^>^v>^^v^^>vv^^v^v<^^<>><v^<^^v<<>^><<v^>vvv<^<v<v^<>><<^^^>>v><v<^>v^<>^v<v<>^>><^^>>^<<<vv>^^^<^<><^v<<<^<>vv<<<^v<^^^^<<^^v<^vv^v>><<<^^>>>vv^vv>>^v^^^^^<<><<v<vv^><^v><><^>^<vvv^>^^><>>>v><^^v>>^^^v<<v<>><<v^>^^^^>v^<^>>^vv>>v^<<^<^>^v><vvv>><<<><v<<<v><^^><<>>v><^v^vv<v^>^<<^<^v>^<><v<<^vv^v>>><vvv><v<><v<<^^^<>v^>v^v<v>>^>^^v>^<>>^^>vv^^^<>^>^vvv^>vv<><<^>v><><<^<v<<<^^v<<>>>><v^^<><^>>><<^>>^>^>>^^v^v^v>^^<^<<<<>v>>v^v<><>^><>>>>v<><<><>vv^><^>>>v^<v^^>vv<v^^v^v>^vv^^v<<^^^^>><><^>^>^>>^^><>v^^v>^>v>>>>v<v<v^^><^>^><^v^<><v
^^^>>>v>v<>>^v>v<<^>^>^vv<<>v<v<>v>^^^<><^<<<<v><^^^<<<v^^>^v>^<>v<^<v<^>v>^<vv^>v<^><v<v>v<<^<>^^<<v>v^^vv<^v>^^><v><>v<<^>><v^>vv<^><<<v>^^v>^<<^<<v^^v><>>^^^>^>>^><v^<>v>^vv^v<><<>>><<v><><>^<<<>^<v<^>v<v^<<^^^v^vv>v><^vv>v<^>v><^v>>^^^^^^>^>^^<<^<^<^^><vv^>v^<v>>v>^<>^v>>^^vv>>v<v<v>>>v>v>v<^^>>>^^v^>v<>^<vvvv><v>v<v<>^<v<<>^>>^<v^^<><>>^<>v^^v<<^>>^>^>vv>><^>^^v^<vv>>v^v<>v><><^vv>>^^^vv<><^^>^^>vv<>^v>><v<vv>^<v^<^^>^<<^^^<^><^^^><v<vv>vv^^vv^^^>^<v^v<^^^v<^<^v>>><>^>><<v<>><><v^^<>^>^>v>^>><>>v<^<>^v<^v>><<^v<vvv<>>>><^v^v^<<vv>>^<v^>^vv<<<^v<v>v>v^v^^vv<v<^v<>v<<^>><v>v>v<^v><^<><^><v>^>^v<>>^<v<><v^v^^v>>vv^^^^<><^vvv^v<<^v<^v>v<vv^v<<^v>^v^^>^>^<^^^v^v<^v><<<^vv^>>^v<^v<<<^<^v^<^vv<^v^^v>v<<<v<<<v>><v^^><^v^<<vvv>>^><<>^>v<>v<v<><^>>>><v<>vv^>vvv<v<^<<>^<<v^v<<<v^vv^<vvv>><v<<^>>v^>v^^^^v<^^^^^>v<<^<>><<vv><^^^<v^^<>vv>v><<<>><>vv<v<v<><v<>vv^<<<^<>v^>>>v<<v<<v^v<^vv>^^<v<^<<>v<<<<^<v<>^<>v><^^<>v^>><^^>>^<v^^><^v>>v<^^^><<vvvv^^^<v^>^>^^v<vv^^<^^<<vv>v>^v<v<<v^^v^^>^v^><v>^<
^<^^<<v<>v<v<<<>v^^^^<>><vv<>vvvvv<^<^<>vv<^v>^>>^v^>>^>><>^^^>^v<<>><^^^>v^>>v<^^v>^>^vv<<vvv^<^^v>v<v>>v^v^<v>>>vv<vv^>^<^<v<>^^v<<vv>v<<v<^^<<>v^v<>v>><^<v<v^>>>><v<<<>vv>^<<><<^<v<v^^^^^<^>>><v><>v>v^^^v<^^vv>>>vv>vv<^>vv>>vv^^>v<<<v^vv>>^^<^>^>vv<v>^v<^>^v>^<vv>>^>>v<^>v<v^>vv<^^^>^^>>v>^<>v>^>v>vv^>>^^<>>v^^^<><v^<vv<><>^<<<<<>>v^v<^<>v^<>^v<v^v>vv<>>^<^<^>v^<^<v^vv>>><v<><><v>>v^<^<<^>v^v>v>>^v><v<^v<^<<^^^<>^<v^^<v^^v><<v<^><v<<v<<<<^^^^>v^^vvv><^^vv^v<<<<>vv<<vvv>v^<<>>v^>vv<>v<><>>>v^<v>>^^^>^v^>v><^><<vv^<>>^<>vv^^>vv>^<^<>vv<<v^>^vv<v<><<v^vv>>>v>^<<>v>><>vv><^vv^>vvv^<^v^vv<^^v^^v<>>^^<<>^<>^<<<v^>^>>>>vvv^>^<<v<>>^>v<><>v^>^^>^>><vv>^<^<v>^<><v<><>^^vv^>^^^<>^v>>vv^><v^v^^>^v^^^v>>^^^>>v>^<>>><<<^v<^v>><<>vvv>^vv>v>^v><<vv^^<<^^^<vv^^^<^<>>^v><vv><><v<^v<><<vv>vv^>>^v>^v><><<vvv<<^<<>v>>vv><<<><<><<^<<vv<vvv<<<<<^>^vv^v>><><^^<<>^vvvv^>>v<^^><v>v^vv<<>^>^^vv<>v><<v>^^<><^<><vvv<^<^^<>^>>^^<^<vvvvv<>^v><vv^<^><^^^<v^>^<^^^v^v>v^<<>v>>vvvv^vv><v<<v<v<vv><<>vv>^^^vv>>v^v>v<<
vv^<<^v><<vvv>>>vv<>^<^><>>^^>^<v><<<<<<^<^<>>>v<<<<><vv^^^^v<<>vv^>v<^v>v>vv>v><>v<v<<v<>^^^><v>vv<<>^^>v^<<><^^vvv^^v^>^<<>v^<>^><>^^>>v>v<v<>^v>^^<^<^^^^>v^v<v><<^<><^>^^v>>v>v<<vv>^>><<<v^><>vv^^v^v>^^<<<<^vv^>>>v<vvv^^<>v<^^v^^^<v<>><<>^^>^v<v<v<<<<<>v^<>v<^<vv^^<>>v^<vv><^^<<>v<^v>^^>vv>>^^v^^>v^<>>>vv>^<v>^v<^^<>^^><<>v<>>v<<>^>>>><^>^<<<>^^<^^<v^v<^><v<<<v^v>><<<^<>v<^><<v>>v<>><><^<v><vv^^>>v>vv>><^>v<>v^<^<v<<^^>v<^^^^<<<>^<<><^>>><^<>^>^^<>v<>v<><v>><v<v><v^^^>^^<>^>>v<^<v>^<^v^vv^><v^^>^^>^<vv<<^^v<><v^v^v^<^^vv^>><^<><<^<v<v<^>^>^<v^<>>^^vv><v<<^vvvv<v^>>v^v<^>>^^>vv^v^>><>><<<<<<^<^>v^<<v>v>v^<v^>>^<<>><<v>>^vv<>><>>^^>v>^>^<vv^<^v>>v>^><^<^<<v^>v>^>>v<vv><>^^^v>><v^><^^>^v^^v>^<^>>>v><<<<><^><<<<vv><>vvv<<v^<><^><vv^<><<<^v<vvv^<<>>v<<v<<>><<^v^v<>v^^>^^vv<v^>^^>v><v^<vv<<<><<<v<^><vvv<vv^^vvv<vvv<^>^>^v<<>^v>vv^><<>><v<^>>^<^>vv^v><>^vv<>vv>^<>>^<^><v^v^v><><v><^v>^^><vv<<<^>>v>v^v^<^vv>>>^^>><^^v^>v<^<<<>><v^<^^v<^v<>vvv<>>>v<<vv<<^v>^<v><^>vv<>><<>^<vvvvv^v><^>^v<<><>
<<>v^^^v<<v<^<<<<<<^vv><>^<>v^><v><v<^<>^vvv<^vv>v^<><^^>v^<v<vv>v^><><<v>>>>><^<vv<v>^>^<<>v><<>>><>>^>v<<>v<<^<^^^<<v^^^<>>v<<<<<v<>^^>^<><<^<v^<>^^<vv>vvv^^v<v>v<v>^<>>^vv^><v<<<<<<v^^v<^v^v^>^^><^^v^<<>>v<^^<^^v^>>^>v<<v<v^<^vvv^<v<>><^v>v><v^<<<^<^vvv^<<v^<>><<>>vv<^<vv^^v<<^><v^v<^^>^vv^^<<>><<><>>v>>vv^>>v^<<v>^v>^^>^^<<^v>>vv<<>>v>>vv<vv^^<>^>^<vv^>v^^><^v<<vv<><<<v<^<^<<><^vv<><>>>>>>^<<>>^>>^^^<v<>><<v><^^^^^>>v<>><><>>><<>><^><^<<^<v^^><v^^^>vv>v><<vv>>^^v^v^><<vv>^^<^>^<<vv><<<v>><<>>><^^v^<>>vv<>><^^^>>^v<^>>>>>v<^v<>^>^<^>^^^v<<^<v>^^^>>vv>>>>v>>^^<>>>^><<><^^^<<>vv^^<>vv^><v^v<>>>v>^v<^v>^<>^<<^^^^v>^^vv>>>>>>^vv<^v^<><>v^><^>><><>><<^v>v<<^v^^<^<^^v^^<>v<^v>v^<v<<><^<><vv^v^^>><<v<v<<v<v>^>v>><^<^^^^v><vv^><<<^^>>>^<vv><<><<^<^<^^>^<^^^>>^^>v><<vv>v<>^>^^^<><>v><<<>^v<>v<>>^^^v<<<<<v^>vv^>>^<^v^<<<^>><v^v^>>^<^^^v<>v>>>vv^<<v<<^vv>^v^^<v<v<>^^^^vv<v<^^^^v<><v>v<>v<<<>>v^v>v<><<>>v^v<><><v<>>v>vvvvvv^^^<<>v<<>^v><<v><<^^^v<<^<>^v<<>^v<^<>vv>vv^vvv>^^>><>^>^^v<<<^v<v^<>^<
"""
directions = [DIRECTION_MAP[d] for d in directions if d in DIRECTION_MAP.keys()]
