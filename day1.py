from collections import Counter
from typing import Tuple, List

DATA_FILE = "./data/day1.txt"


def get_ids() -> Tuple[List[int], List[int]]:
    ids1, ids2 = [], []
    with open(DATA_FILE, "r") as f:
        for line in f:
            id1, id2 = line.split()
            ids1.append(int(id1))
            ids2.append(int(id2))
    return (ids1, ids2)


def calculate_total_distance(
    ids1: list[int],
    ids2: list[int],
) -> int:
    ids1.sort()
    ids2.sort()
    total = 0
    for id1, id2 in zip(ids1, ids2):
        total += abs(id1 - id2)
    return total


def calculate_similarity_score(
    ids1: list[int],
    ids2: list[int],
) -> int:
    counts = Counter(ids2)
    total = 0
    for id in ids1:
        total += id * counts[id]
    return total


ids1, ids2 = get_ids()
print(calculate_total_distance(ids1, ids2))
print(calculate_similarity_score(ids1, ids2))
