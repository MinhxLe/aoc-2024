from dataclasses import dataclass
import abc
from typing import Literal
import re


class Node(abc.ABC):
    @abc.abstractmethod
    def value(self) -> Literal[0, 1]:
        pass


@dataclass
class ValNode(Node):
    _value: Literal[0, 1]

    def value(self) -> Literal[0, 1]:
        return self._value


@dataclass
class OpNode(Node):
    lhs: Node
    rhs: Node
    operator: Literal["AND", "OR", "XOR"]

    def value(self) -> Literal[0, 1]:
        operator_fn = {
            "AND": int.__and__,
            "OR": int.__or__,
            "XOR": int.__xor__,
        }[self.operator]
        return operator_fn(self.lhs.value(), self.rhs.value())


@dataclass
class NoopNode:
    node: Node | None = None

    def value(self) -> bool:
        if self.node is None:
            raise ValueError("node is symbolic")
        else:
            return self.node.value()


def parse_nodes(fname) -> dict[str, Node]:
    nodes = dict()
    with open(fname) as f:
        for line in f:
            name, new_node = None, None
            if (match := re.match(r"([a-z0-9]{3}): ([0,1])", line)) is not None:
                name, val = match.groups()
                new_node = ValNode(int(val))
            elif (
                match := re.match(
                    r"([a-z0-9]{3}) (XOR|AND|OR) ([a-z0-9]{3}) -> ([a-z0-9]{3})", line
                )
            ) is not None:
                lhs, operator, rhs, name = match.groups()
                if lhs not in nodes:
                    nodes[lhs] = NoopNode()
                if rhs not in nodes:
                    nodes[rhs] = NoopNode()
                new_node = OpNode(nodes[lhs], nodes[rhs], operator)
            if name is not None:
                if name not in nodes:
                    nodes[name] = new_node
                else:
                    assert isinstance(nodes[name], NoopNode)
                    nodes[name].node = new_node
    for name, node in nodes.items():
        if isinstance(node, NoopNode):
            assert node.node is not None
    return nodes


def part_1():
    nodes = parse_nodes("./data/day24.txt")
    z_node_names = sorted([n for n in nodes if n[0] == "z"], reverse=True)
    z_values = [nodes[n].value() for n in z_node_names]
    print(int("".join([str(i) for i in z_values]), 2))
