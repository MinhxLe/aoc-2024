from dataclasses import dataclass
from typing import Literal, Tuple, TypedDict
import re
import copy

from range import Range


class Part(TypedDict):
    x: int
    m: int
    a: int
    s: int


class PartSet(TypedDict):
    x: Range
    m: Range
    a: Range
    s: Range


def get_rating(part: Part) -> int:
    rating = 0
    for i in part.values():
        rating += i
    return rating


def compute_count(part_set) -> int:
    total = 1
    for r in part_set.values():
        total *= r.end - r.start - 1
    return total


@dataclass
class Action:
    type_: Literal["accept", "reject", "reroute"]
    next_workflow: str | None = None


@dataclass
class Rule:
    compare_field: Literal["x", "m", "a", "x"]
    cond: Literal["<", ">"]
    threshold: int
    action: Action

    def apply_action(self, part: Part) -> Action | None:
        val = part[self.compare_field]
        triggered = False
        if self.cond == "<":
            if val < self.threshold:
                triggered = True
        elif self.cond == ">":
            if val > self.threshold:
                triggered = True
        else:
            raise ValueError
        if triggered:
            return self.action
        else:
            return None

    def apply_action_to_set(
        self, part_set: PartSet
    ) -> list[Tuple[PartSet, Action | None]]:
        pass
        range_to_split = part_set[self.compare_field]
        if self.cond == "<":
            include_start = range_to_split.start
            include_end = min(self.threshold - 1, range_to_split.end)
            exclude_start = max(self.threshold, range_to_split.start)
            exclude_end = range_to_split.end
        elif self.cond == ">":
            include_start = max(self.threshold + 1, range_to_split.start)
            include_end = range_to_split.end
            exclude_start = range_to_split.start
            exclude_end = min(range_to_split.end, self.threshold)
        else:
            raise ValueError

        part_sets_and_actions = []
        if include_start < include_end:
            include_part_set = copy.copy(part_set)
            include_part_set[self.compare_field] = Range(include_start, include_end)
            part_sets_and_actions.append((include_part_set, self.action))

        if exclude_start < exclude_end:
            exclude_part_set = copy.copy(part_set)
            exclude_part_set[self.compare_field] = Range(exclude_start, exclude_end)
            part_sets_and_actions.append((exclude_part_set, None))

        return part_sets_and_actions


@dataclass
class Workflow:
    id: str
    rules: list[Rule]
    default_action: Action

    def apply_action(self, part: Part) -> Action:
        for rule in self.rules:
            next_action = rule.apply_action(part)
            if next_action is not None:
                return next_action
        return self.default_action

    def apply_action_to_set(
        self, initial_part_set: PartSet
    ) -> list[Tuple[PartSet, Action]]:
        all_part_sets_and_actions = []
        part_sets = [initial_part_set]
        for rule in self.rules:
            next_part_sets = []
            for part_set in part_sets:
                for next_part_set, action in rule.apply_action_to_set(part_set):
                    if action is None:
                        next_part_sets.append(next_part_set)
                    else:
                        all_part_sets_and_actions.append((next_part_set, action))
            part_sets = next_part_sets
        return all_part_sets_and_actions + [
            (part_set, self.default_action) for part_set in part_sets
        ]


@dataclass
class WorkflowSet:
    workflows: dict[str, Workflow]

    def apply_action(self, part: Part) -> Action:
        action = self.workflows["in"].apply_action(part)
        while action.type_ != "accept" and action.type_ != "reject":
            assert action.type_ == "reroute"
            assert action.next_workflow is not None
            action = self.workflows[action.next_workflow].apply_action(part)
        return action

    def apply_action_to_set(
        self, initial_part_set: PartSet
    ) -> list[Tuple[PartSet, Action]]:
        terminated_part_set_and_actions = []

        part_set_and_actions = self.workflows["in"].apply_action_to_set(
            initial_part_set
        )
        while len(part_set_and_actions) > 0:
            part_set, action = part_set_and_actions.pop()
            if action.type_ == "accept" or action.type_ == "reject":
                terminated_part_set_and_actions.append((part_set, action))
            else:
                assert action.type_ == "reroute"
                assert action.next_workflow is not None
                part_set_and_actions.extend(
                    self.workflows[action.next_workflow].apply_action_to_set(part_set)
                )
        return terminated_part_set_and_actions


def parse_part(s) -> Part:
    s = s[1:-1]  # remove brackets
    part = dict()
    for val_str in s.split(","):
        key, val_str = val_str.split("=", 1)
        part[key] = int(val_str)
    return part


def parse_action(s) -> Action:
    if s == "A":
        return Action("accept")
    elif s == "R":
        return Action("reject")
    else:
        return Action("reroute", s)


def parse_rule(s) -> Rule:
    cond_str, action_str = s.split(":", 1)
    return Rule(
        compare_field=cond_str[0],
        cond=cond_str[1],
        threshold=int(cond_str[2:]),
        action=parse_action(action_str),
    )


def parse_workflow(s) -> Workflow:
    match = re.match(r"(\w+){(.*)}", s)
    assert match is not None
    id, rules_str = match.groups()
    rules = rules_str.split(",")
    # the last "rule" is actually a default action
    return Workflow(
        id=id,
        rules=[parse_rule(r) for r in rules[:-1]],
        default_action=parse_action(rules[-1]),
    )


def parse(fname) -> Tuple[WorkflowSet, list[Part]]:
    workflows = []
    parts = []
    with open(fname) as f:
        for line in f:
            line = line.strip()
            if re.match(r"\w+{.*}", line):
                workflows.append(parse_workflow(line))
            elif re.match(r"{.*}", line):
                parts.append(parse_part(line))
    workflow_set = WorkflowSet({w.id: w for w in workflows})
    return workflow_set, parts


if __name__ == "__main__":
    fname = "./y2023/data/d19.txt"
    ws, parts = parse(fname)
    # part 1
    total = 0
    for part in parts:
        if ws.apply_action(part).type_ == "accept":
            total += get_rating(part)
    print(total)

    fname = "./y2023/data/d19_small.txt"
    ws, parts = parse(fname)

    initial_part_set = dict(
        x=Range(1, 4001),
        m=Range(1, 4001),
        a=Range(1, 4001),
        s=Range(1, 4001),
    )
    total = 0
    for part_set, action in ws.apply_action_to_set(initial_part_set):
        if action.type_ == "accept":
            print(part_set)
            total += compute_count(part_set)
