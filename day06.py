#!/usr/bin/env python
import math


def part1():
    time = [57, 72, 69, 92]
    distance = [291, 1172, 1176, 2026]

    prod_of_ways_to_win = 1
    for available_time, distance_record in zip(time, distance):
        num_ways_to_win = 0
        for hold_time in range(1, available_time):
            velocity = hold_time
            distance = velocity * (available_time - hold_time)

            if distance > distance_record:
                num_ways_to_win += 1

        prod_of_ways_to_win *= num_ways_to_win

    return prod_of_ways_to_win


def part2():
    time = int("".join(map(str, [57, 72, 69, 92])))
    distance = int("".join(map(str, [291, 1172, 1176, 2026])))

    p = -time
    q = distance

    x1 = -p / 2 + math.sqrt((p / 2) ** 2 - q)
    x2 = -p / 2 - math.sqrt((p / 2) ** 2 - q)

    num_ways = math.floor(x1) - math.ceil(x2) + 1
    return num_ways


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
