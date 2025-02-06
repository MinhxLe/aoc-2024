from dataclasses import dataclass


@dataclass
class Range:
    start: float
    end: float  # exclusive

    def __post_init__(self):
        assert self.start <= self.end

    def contains(self, x: float):
        return self.start <= x < self.end
