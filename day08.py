#!/usr/bin/env python
import pytest
import re

from dataclasses import dataclass
from itertools import cycle


@dataclass
class TreeNode:
    left: str
    right: str


def parse(inputs: str) -> tuple[str, dict[str, TreeNode]]:
    lines = inputs.splitlines()
    directions = lines[0]
    
    node_pattern = re.compile(r"^([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)$")
    nodes = {}
    for line in lines[1:]:
        m = node_pattern.match(line)
        if not m:
            continue

        name, left, right = m.groups()
        node = TreeNode(left, right)
        nodes[name] = node

    return directions, nodes


def perform_step(current_node: str, direction: str, nodes: dict[str, TreeNode]) -> str:
    if direction == "L":
        return nodes[current_node].left
    elif direction == "R":
        return nodes[current_node].right
    else:
        raise RuntimeError("Unknown direction")


def part1(inputs: str) -> int | None:
    directions, nodes = parse(inputs)

    current_node = "AAA"
    for step, direction in enumerate(cycle(directions)):
        if current_node == "ZZZ":
            return step

        current_node = perform_step(current_node, direction, nodes)

    return None


def find_cycle(starting_node: str, directions: str, nodes: dict[str, TreeNode]) -> tuple[int, int] | None:
    current_node = starting_node
    visit_history = [(len(directions), current_node)]

    for idx, direction in cycle(enumerate(directions, 1)):
        current_node = perform_step(current_node, direction, nodes)

        if (idx, current_node) in visit_history:
            cycle_start = visit_history.index((idx, current_node))
            cycle_length = len(visit_history) - cycle_start
            return cycle_start, cycle_length
        else:
            visit_history.append((idx, current_node))

    return None


def part2(inputs: str) -> int:
    directions, nodes = parse(inputs)
    current_nodes = [node for node in nodes if node.endswith("A")]

    # Find cycles
    cycle_lengths = []
    for node in current_nodes:
        c = find_cycle(node, directions, nodes)
        assert c is not None
        cycle_start, cycle_length = c
        assert cycle_length % len(directions) == 0

        current_node = node

        steps = None
        for step, direction in enumerate(cycle(directions)):
            if current_node.endswith("Z"):
                steps = step
                break

            current_node = perform_step(current_node, direction, nodes)

        # For some reason the first **Z is always equal to the length of the cycle
        print(f"{node} -> {cycle_start = } {cycle_length = } {steps = }")
        cycle_lengths.append(cycle_length)

    import math

    return math.lcm(*cycle_lengths)


TEST_INPUT_1 = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""


TEST_INPUT_2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

TEST_INPUT_3 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


@pytest.mark.parametrize(
    "input,expected",
    [
        (TEST_INPUT_1, 2),
        (TEST_INPUT_2, 6),
    ],
    ids=["TEST_INPUT_1", "TEST_INPUT_2"],
)
def test_part1(input: str, expected: int) -> None:
    assert part1(input) == expected


def test_part2() -> None:
    assert part2(TEST_INPUT_3) == 6


def test_cycle_start0_len3() -> None:
    test_input = """\
LLL

AAA = (BBB, XXX)
BBB = (CCC, XXX)
CCC = (AAA, XXX)"""
    directions, nodes = parse(test_input)
    assert find_cycle("AAA", directions, nodes) == (0, 3)


def test_cycle_start2_len12() -> None:
    test_input = """\
LLL

AAA = (BBB, XXX)
BBB = (CCC, XXX)
CCC = (DDD, XXX)
DDD = (EEE, XXX)
EEE = (FFF, XXX)
FFF = (CCC, XXX)"""
    directions, nodes = parse(test_input)
    assert find_cycle("AAA", directions, nodes) == (2, 12)


if __name__ == "__main__":
    with open("inputs/day08.txt") as fin:
        inputs = fin.read()

    print(f"Part 1: {part1(inputs)}")
    print(f"Part 2: {part2(inputs)}")
