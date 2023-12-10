#!/usr/bin/env python
import pytest
import re

from dataclasses import dataclass
from itertools import cycle


@dataclass
class TreeNode:
    left: str
    right: str


def parse(inputs):
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


def perform_step(current_node, direction, nodes):
    if direction == "L":
        return nodes[current_node].left
    elif direction == "R":
        return nodes[current_node].right
    else:
        raise RuntimeError("Unknown direction")


def part1(inputs):
    directions, nodes = parse(inputs)

    current_node = "AAA"
    for step, direction in enumerate(cycle(directions)):
        if current_node == "ZZZ":
            return step

        current_node = perform_step(current_node, direction, nodes)


def part2(inputs):
    directions, nodes = parse(inputs)

    current_nodes = [node for node in nodes if node.endswith("A")]
    for step, direction in enumerate(cycle(directions)):
        if all(node.endswith("Z") for node in current_nodes):
            return step
        
        current_nodes = [perform_step(node, direction, nodes) for node in current_nodes]


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
def test_part1(input, expected):
    assert part1(input) == expected


def test_part2():
    assert part2(TEST_INPUT_3) == 6


if __name__ == "__main__":
    with open("inputs/day08.txt") as fin:
        inputs = fin.read()

    print(f"Part 1: {part1(inputs)}")
    print(f"Part 2: {part2(inputs)}")
