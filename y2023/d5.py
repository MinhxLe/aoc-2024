from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Range:
    start: int
    end: int

    def __post_init__(self):
        assert self.start <= self.end

    @classmethod
    def empty(cls):
        return Range(0, 0)

    def __len__(self):
        return self.end - self.start

    def contains(self, i: int) -> bool:
        return self.start <= i < self.end

    def __and__(self, that: "Range") -> "Range":
        if self.end <= that.start:
            return Range.empty()
        elif self.start >= that.end:
            return Range.empty()
        else:
            return Range(
                max(self.start, that.start),
                min(self.end, that.end),
            )

    def __sub__(self, that: "Range") -> set["Range"]:
        if self.end <= that.start:
            return {self}
        elif self.start >= that.end:
            return {self}
        else:
            return {
                Range(self.start, that.start),
                Range(that.end, self.end),
            }


@dataclass
class Map:
    input_space: Range
    offset: int

    def map_ranges(self, rs: list[Range]) -> list[Range]:
        pass

    def map_range(self, r: Range) -> list[Range]:
        pass


@dataclass
class RangeSet:
    ranges: list[Range]


@dataclass
class RangeMap:
    input_space: Range
    offset: int

    def map_elm(self, x: int) -> int:
        assert self.input_space.contains(x)
        return x + self.offset


@dataclass
class UnionMap:
    maps: list[RangeMap]

    def map_elm(self, x: int) -> int:
        for map_ in self.maps:
            if map_.input_space.contains(x):
                return map_.map_elm(x)
        return x


def parse_file(fname):
    with open(fname) as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]
    seeds = [int(i) for i in lines[0][len("seeds: ") :].split(" ")]
    maps = []
    curr_map = None
    for line in lines:
        if (match := re.match(r"(\w*)-to-(\w*) map:", line)) is not None:
            if curr_map is not None:
                maps.append(curr_map)
            domain_name, _ = match.groups()
            curr_map = UnionMap([])
        elif (match := re.match(r"(\d*) (\d*) (\d*)", line)) is not None:
            output_start_str, start_str, len_str = match.groups()
            start = int(start_str)
            end = start + int(len_str)
            offset = int(output_start_str) - start
            curr_map.maps.append(RangeMap(Range(start, end), offset))
        else:
            continue
    if curr_map is not None:
        maps.append(curr_map)
    return seeds, maps


def p1(seeds, maps: list[UnionMap]):
    final_outputs = []
    for seed in seeds:
        output = seed
        for map_ in maps:
            output = map_.map_elm(output)
        final_outputs.append(output)
    print(min(final_outputs))


def test_range_and():
    assert (Range(0, 1) & Range(-1, 0)) == Range(0, 0)
    assert (Range(0, 5) & Range(2, 4)) == Range(2, 4)


def test_range_sub():
    assert (Range(0, 5) - Range(-1, 0)) == {Range(0, 5)}
    assert (Range(0, 5) - Range(6, 7)) == {Range(0, 5)}
    assert (Range(0, 5) - Range(5, 7)) == {Range(0, 5)}


def test_range_map():
    m = RangeMap(Range(0, 3), 3)
    assert m.map_elm(0) == 3
    assert m.map_elm(1) == 4


def test_union_map():
    m = UnionMap([RangeMap(Range(0, 3), 3)])
    assert m.map_elm(0) == 3
    assert m.map_elm(4) == 4
