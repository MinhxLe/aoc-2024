from dataclasses import dataclass
import re


@dataclass
class Round:
    n_blue: int
    n_red: int
    n_green: int


@dataclass
class Game:
    id: int
    rounds: list[Round]


def is_possible(
    game: Game,
    max_red: int,
    max_green: int,
    max_blue: int,
) -> bool:
    return all(
        [
            r.n_blue <= max_blue and r.n_green <= max_green and r.n_red <= max_red
            for r in game.rounds
        ]
    )


def parse_round(round_str) -> Round:
    round_str = round_str.strip()
    counts = dict()
    for cube_str in round_str.split(", "):
        n, color = cube_str.split(" ")
        counts[color] = int(n)
    return Round(
        n_blue=counts.get("blue", 0),
        n_green=counts.get("green", 0),
        n_red=counts.get("red", 0),
    )


def parse_games(fname: str) -> list[Game]:
    games = []
    with open(fname) as f:
        for line in f:
            line = line.strip()
            game_str, round_str = line.split(":", 1)
            id = int(game_str[len("Game ") :])
            rounds = [parse_round(s) for s in round_str.split("; ")]
            games.append(Game(id, rounds))
    return games


def p1():
    games = parse_games("./y2023/data/d2.txt")
    total = 0
    for game in games:
        if is_possible(game, 12, 13, 14):
            total += game.id
    print(total)


def p2():
    games = parse_games("./y2023/data/d2.txt")
    total = 0
    for game in games:
        red_needed = max([r.n_red for r in game.rounds])
        blue_needed = max([r.n_blue for r in game.rounds])
        green_needed = max([r.n_green for r in game.rounds])
        total += red_needed * blue_needed * green_needed
    print(total)
