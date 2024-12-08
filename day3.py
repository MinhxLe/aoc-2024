import re


def part1(text: str):
    pattern = r"mul\(\d{1,3},\d{1,3})"
    matches = re.findall(pattern, text)
