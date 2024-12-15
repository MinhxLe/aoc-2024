from collections import Counter, defaultdict
import functools


def transform_stone(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    stone_str = str(stone)
    if (len(stone_str) % 2) == 0:
        half_len = len(stone_str) // 2
        return [int(stone_str[:half_len]), int(stone_str[half_len:])]
    return [2024 * stone]


def transform_stones(stones: list[int], n: int) -> int:
    counts = Counter(stones)
    for _ in range(n):
        new_counts = defaultdict(int)
        for stone, count in counts.items():
            new_stones = transform_stone(stone)
            for new_stone in new_stones:
                new_counts[new_stone] += count
        counts = new_counts

    return sum([x for x in counts.values()])


test_stones = [125, 17]
stones = [30, 71441, 3784, 580926, 2, 8122942, 0, 291]
print(transform_stones(test_stones, 25))
print(transform_stones(stones, 25))
print(transform_stones(stones, 75))
