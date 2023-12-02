#!/usr/bin/env python
import re
from dataclasses import dataclass


@dataclass
class Game:
    id: int
    draws: list[dict[str, int]]


def parse(inputs: str):
    pattern = re.compile(r"^Game (\d+): (.*)$")
    pattern_color = re.compile(r"(\d+) (red|green|blue)")

    games = []
    for line in inputs.splitlines():
        m = pattern.match(line)
        game_id, cubes = m.groups()

        draws = []
        for draw in cubes.split("; "):
            color_counts = {
                m.group(2): int(m.group(1)) for m in pattern_color.finditer(draw)
            }
            draws.append(color_counts)

        game = Game(int(game_id), draws)
        games.append(game)

    return games


def possible_game(game: Game, red: int, green: int, blue: int):
    for draw in game.draws:
        if (
            draw.get("red", 0) > red
            or draw.get("green", 0) > green
            or draw.get("blue", 0) > blue
        ):
            return False

    return True


def part1(games: list[Game]):
    red = 12
    green = 13
    blue = 14

    s = 0
    for game in games:
        if possible_game(game, red, green, blue):
            s += game.id

    return s


def part2(games):
    total_power = 0
    for game in games:
        max_red = max(draw.get("red", 0) for draw in game.draws)
        max_green = max(draw.get("green", 0) for draw in game.draws)
        max_blue = max(draw.get("blue", 0) for draw in game.draws)

        total_power += max_red * max_green * max_blue

    return total_power


if __name__ == "__main__":
    with open("inputs/day02.txt") as fin:
        inputs = fin.read()

    games = parse(inputs)
    print(f"Part 1: {part1(games)}")
    print(f"Part 2: {part2(games)}")
