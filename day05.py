import re
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class MapEntry:
    destination_range_start: int
    source_range_start: int
    range_length: int

    def contains(self, num: int) -> bool:
        return (
            self.source_range_start <= num
            and num < self.source_range_start + self.range_length
        )


def parse_seeds(inputs: str) -> list[int]:
    pattern_seeds = re.compile(r"^seeds: (.*)$", re.MULTILINE)
    m = pattern_seeds.search(inputs)
    assert m is not None 
    seeds = list(map(int, m.group(1).split()))

    return seeds


def parse_maps(inputs: str) -> defaultdict[tuple[str, str], MapEntry]:
    pattern_map = re.compile(r"^(\w+)-to-(\w+) map:$")
    pattern_map_entry = re.compile(r"^(\d+) (\d+) (\d+)$")
    maps = defaultdict(list)

    current_section = None
    for line in inputs.splitlines():
        m = pattern_map.match(line)
        if m:
            current_section = (m.group(1), m.group(2))

        m = pattern_map_entry.match(line)
        if m:
            dst_start = int(m.group(1))
            src_start = int(m.group(2))
            length = int(m.group(3))
            maps[current_section].append(MapEntry(dst_start, src_start, length))

    return maps


def part1(inputs: str) -> int:
    seeds = parse_seeds(inputs)
    maps = parse_maps(inputs)

    locations = []
    for seed in seeds:
        state = "seed"
        num = seed
        while state != "location":
            (destination,) = [key[1] for key in maps if key[0] == state]
            entries = maps[state, destination]

            for entry in entries:
                if entry.contains(num):
                    num = num - entry.source_range_start + entry.destination_range_start
                    break

            state = destination

        locations.append(num)

    return min(locations)


def part2(inputs: str) -> None:
    seeds = parse_seeds(inputs)
    maps = parse_maps(inputs)

    seed_range_start = seeds[::2]
    seed_range_length = seeds[1::2]


if __name__ == "__main__":
    with open("inputs/day05.txt") as fin:
        inputs = fin.read()

    print(f"Part 1: {part1(inputs)}")
    print(f"Part 2: {part2(inputs)}")
