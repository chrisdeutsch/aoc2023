import pytest
from collections import OrderedDict


def parse(inputs: str) -> list[str]:
    return [split.strip() for split in inputs.split(",")]


def aoc_hash(string: str) -> int:
    val = 0
    for char in string:
        val += ord(char)
        val *= 17
        val %= 256

    return val


def part1(inputs: str) -> int:
    sum = 0
    for init_seq in parse(inputs):
        if init_seq == "\n":
            print("BLAA")
        sum += aoc_hash(init_seq)
    return sum


def run_instructions(inputs: str) -> list[OrderedDict[str, int]]:
    boxes: list[OrderedDict[str, int]] = [OrderedDict() for _ in range(256)]

    for instruction in parse(inputs):
        if "=" in instruction:
            lense_name, focal_length = instruction.split("=")
            h = aoc_hash(lense_name)
            boxes[h][lense_name] = int(focal_length)
        elif instruction.endswith("-"):
            lense_name = instruction[:-1]
            h = aoc_hash(lense_name)
            if lense_name in boxes[h]:
                del boxes[h][lense_name]
        else:
            raise RuntimeError("Unknown instruction")

    return boxes


def part2(inputs: str) -> int:
    boxes = run_instructions(inputs)

    total = 0
    for box_num, box in enumerate(boxes):
        for slot_num, lense in enumerate(box, 1):
            focal_length = box[lense]
            total += (box_num + 1) * slot_num * focal_length
    
    return total


@pytest.mark.parametrize(
    "string, expected",
    [
        ("HASH", 52),
        ("rn=1", 30),
        ("cm-", 253),
        ("qp=3", 97),
        ("pc-", 48),
    ],
)
def test_hash(string: str, expected: int) -> None:
    assert aoc_hash(string) == expected


TEST_INPUT = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def test_part1() -> None:
    assert part1(TEST_INPUT) == 1320


def test_run_instructions() -> None:
    boxes = run_instructions(TEST_INPUT)
    assert boxes[0] == OrderedDict(rn=1, cm=2)
    assert boxes[3] == OrderedDict(ot=7, ab=5, pc=6)


def test_part2() -> None:
    assert part2(TEST_INPUT) == 145


if __name__ == "__main__":
    with open("inputs/day15.txt") as fin:
        inputs = fin.read()

    print(f"Part 1: {part1(inputs)}")
    print(f"Part 2: {part2(inputs)}")
