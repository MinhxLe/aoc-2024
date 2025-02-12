import re
import abc
from dataclasses import dataclass, field
from collections import deque


class Node(abc.ABC):
    @abc.abstractmethod
    def process(self, upstream_node: str, value: bool) -> bool | None: ...


@dataclass
class FlipFlopNode(Node):
    is_on: bool = field(init=False, default=False)

    def process(self, upstream_node: str, value: bool) -> bool | None:
        pulse = None
        if not value:
            self.is_on = not self.is_on
            pulse = self.is_on
        return pulse


@dataclass
class AndNode(Node):
    memory: dict[str, bool] = field(init=False, default_factory=dict)

    def add_upstream(self, upstream: str):
        self.memory[upstream] = False

    def process(self, upstream_node: str, value: bool) -> bool | None:
        assert upstream_node in self.memory
        self.memory[upstream_node] = value
        if all(self.memory.values()):
            return False
        else:
            return True


@dataclass
class BroadcastNode(Node):
    def process(self, upstream_node: str, value: bool) -> bool | None:
        return value


@dataclass
class ButtonNode(Node):
    def process(self, upstream_node: str, value: bool) -> bool | None:
        return False


@dataclass
class NoopNode(Node):
    def process(self, upstream_node: str, value: bool) -> bool | None:
        return None


@dataclass
class Event:
    upstream: str
    value: bool
    downstream: str


@dataclass
class ModuleGraph:
    nodes: dict[str, Node]
    edges: dict[str, list[str]]

    def __post_init__(self):
        # add button nodes
        self.nodes["button"] = ButtonNode()
        self.edges["button"] = ["broadcast"]

        # add memory for and nodes
        for upstream, downtreams in self.edges.items():
            for downstream in downtreams:
                if downstream not in self.nodes:
                    self.nodes[downstream] = NoopNode()
                else:
                    if isinstance(self.nodes[downstream], AndNode):
                        self.nodes[downstream].add_upstream(upstream)

    def push(self) -> list[Event]:
        process_queue = deque([Event("", False, "button")])
        events = []
        while len(process_queue) > 0:
            curr_event = process_queue.popleft()
            upstream_node = curr_event.upstream
            target_node = curr_event.downstream
            value = curr_event.value
            next_value = self.nodes[target_node].process(upstream_node, value)
            if next_value is not None:
                for next_target_node in self.edges[target_node]:
                    event = Event(target_node, next_value, next_target_node)
                    events.append(event)
                    process_queue.append(event)
        return events


def parse_file(fname) -> ModuleGraph:
    nodes = dict()
    edges = dict()
    with open(fname) as f:
        for line in f:
            line = line.strip()
            if (match := re.match(r"broadcaster -> (.*)", line)) is not None:
                (downstream_str,) = match.groups()
                nodes["broadcast"] = BroadcastNode()
                edges["broadcast"] = downstream_str.split(", ")
            elif (match := re.match(r"([%,&])(\w*) -> (.*)", line)) is not None:
                (
                    type_str,
                    upstream_str,
                    downstream_str,
                ) = match.groups()
                nodes[upstream_str] = {"&": AndNode, "%": FlipFlopNode}[type_str]()
                edges[upstream_str] = downstream_str.split(", ")
            else:
                raise ValueError("parsing failed")
    return ModuleGraph(nodes, edges)


def part_1(fname):
    g = parse_file(fname)
    total_false_count = 0
    total_true_count = 0
    for _ in range(1000):
        events = g.push()
        false_count = len([e for e in events if not e.value])
        true_count = len(events) - false_count
        total_false_count += false_count
        total_true_count += true_count
    return total_true_count * total_false_count
