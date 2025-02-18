from typing import Callable, TypeVar

T = TypeVar("T")


def parse_file(fname: str, parse_line_fn: Callable[[str], T]) -> list[T]:
    objs = []
    with open(fname) as f:
        for line in f:
            line = line.strip()
            objs.append(parse_line_fn(line))
    return objs
