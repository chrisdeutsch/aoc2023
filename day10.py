#!/usr/bin/env python
import pytest

from dataclasses import dataclass
from typing import Self


@dataclass
class PathNode:
    coordinates: tuple[int, int]
    prev: Self | None
    next: Self | None


def pipe_connections(char):
    match char:
        case "|":
            return ("N", "S")
        case "-":
            return ("E", "W")
        case "L":
            return ("N", "E")
        case "J":
            return ("N", "W")
        case "7":
            return ("S", "W")
        case "F":
            return ("E", "S")
        case _:
            return tuple()


def find_start(maze):
    for row_num, row in enumerate(maze):
        try:
            index = row.index("S")
            return row_num, index
        except ValueError:
            continue


def walk(maze, start):
    x, y = start

    # Determine current direction
    current_direction = None
    if "S" in pipe_connections(maze[x - 1][y]):
        current_direction = "N"
    elif "W" in pipe_connections(maze[x][y + 1]):
        current_direction = "E"
    elif "N" in pipe_connections(maze[x + 1][y]):
        current_direction = "S"
    elif "E" in pipe_connections(maze[x][y - 1]):
        current_direction = "W"

    path = [start]
    while True:
        x_next, y_next = path[-1]
        match current_direction:
            case "N":
                x_next -= 1
            case "E":
                y_next += 1
            case "S":
                x_next += 1
            case "W":
                y_next -= 1

        if (x_next, y_next) == start:
            break

        # Determine direction after move
        next_direction = None
        connections = pipe_connections(maze[x_next][y_next])

        match current_direction:
            case "N":
                (next_direction,) = [c for c in connections if c != "S"]
            case "E":
                (next_direction,) = [c for c in connections if c != "W"]
            case "S":
                (next_direction,) = [c for c in connections if c != "N"]
            case "W":
                (next_direction,) = [c for c in connections if c != "E"]

        current_direction = next_direction
        path.append((x_next, y_next))

    return path


def part1(inputs):
    maze = list(map(list, inputs.splitlines()))
    start = find_start(maze)
    path = walk(maze, start)
    return len(path) // 2


def part2(inputs):
    maze = list(map(list, inputs.splitlines()))
    start = find_start(maze)
    path = walk(maze, start)

    return 0


LOOP_1 = """\
.....
.S-7.
.|.|.
.L-J.
....."""

LOOP_2 = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

LOOP_3 = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

LOOP_4 = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

LOOP_5 = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

LOOP_6 = """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""


@pytest.mark.parametrize(
    "inputs",
    [
        LOOP_1,
        LOOP_2,
    ],
    ids=["loop1", "loop2"],
)
def test_simple_loop(inputs):
    maze = list(map(list, inputs.splitlines()))
    start = find_start(maze)
    path = walk(maze, start)

    assert path == [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (2, 1)]


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (LOOP_2, 4),
        (LOOP_3, 8),
    ],
    ids=["loop2", "loop3"],
)
def test_farthest_point(inputs, expected):
    assert part1(inputs) == expected


@pytest.mark.parametrize(
    "inputs, expected",
    [(LOOP_4, 4), (LOOP_5, 8), (LOOP_6, 10)],
    ids=["loop4", "loop5", "loop6"],
)
def test_tiles_contained(inputs, expected):
    assert part2(inputs) == expected


if __name__ == "__main__":
    with open("inputs/day10.txt") as fin:
        inputs = fin.read()

    print(f"Part 1: {part1(inputs)}")
