from enum import Enum, auto
from typing import Literal, Tuple
from dataclasses import dataclass


class Move(Enum):
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()


@dataclass
class Round:
    move: Move
    opponent_move: Move


def get_response_move(move: Move, type_: Literal["draw", "win", "lose"]) -> Move:
    win_map = {
        Move.ROCK: Move.PAPER,
        Move.PAPER: Move.SCISSORS,
        Move.SCISSORS: Move.ROCK,
    }
    lose_map = {v: k for k, v in win_map.items()}
    if type_ == "draw":
        return move
    elif type_ == "lose":
        return lose_map[move]
    elif type_ == "win":
        return win_map[move]
    else:
        raise ValueError


def calculate_score(move: Move, opponent_move: Move) -> int:
    win_value = 6
    draw_value = 3
    lose_value = 0

    move_score = {
        Move.ROCK: 1,
        Move.PAPER: 2,
        Move.SCISSORS: 3,
    }[move]

    round_score = {
        Move.ROCK: {
            Move.ROCK: draw_value,
            Move.PAPER: lose_value,
            Move.SCISSORS: win_value,
        },
        Move.PAPER: {
            Move.ROCK: win_value,
            Move.PAPER: draw_value,
            Move.SCISSORS: lose_value,
        },
        Move.SCISSORS: {
            Move.ROCK: lose_value,
            Move.PAPER: win_value,
            Move.SCISSORS: draw_value,
        },
    }[move][opponent_move]
    return move_score + round_score


def parse_file(fname) -> list[Round]:
    rounds = []
    with open(fname) as f:
        for line in f:
            line = line.strip()
            opponent_move = {
                "A": Move.ROCK,
                "B": Move.PAPER,
                "C": Move.SCISSORS,
            }[line[0]]
            move = {
                "X": Move.ROCK,
                "Y": Move.PAPER,
                "Z": Move.SCISSORS,
            }[line[-1]]
            rounds.append(Round(move, opponent_move))
    return rounds


def parse_file2(fname) -> list[Round]:
    rounds = []
    with open(fname) as f:
        for line in f:
            line = line.strip()
            opponent_move = {
                "A": Move.ROCK,
                "B": Move.PAPER,
                "C": Move.SCISSORS,
            }[line[0]]
            move = {
                "X": get_response_move(opponent_move, "lose"),
                "Y": get_response_move(opponent_move, "draw"),
                "Z": get_response_move(opponent_move, "win"),
            }[line[-1]]
            rounds.append(Round(move, opponent_move))
    return rounds


def total_score(rounds: list[Round]):
    return sum([calculate_score(r.move, r.opponent_move) for r in rounds])


if __name__ == "__main__":
    rounds = parse_file("y2022/data/d2.txt")
    total_score(rounds)

    rounds2 = parse_file2("y2022/data/d2.txt")
