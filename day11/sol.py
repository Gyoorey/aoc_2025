from collections import defaultdict
from typing import Dict, List

# apply dynamic programming to solve the problem
memory_table: Dict[int, Dict[int, int]] = defaultdict(lambda: defaultdict(int))


def apply_rules(stone: int):
    if stone == 0:
        return [1]
    str_stone = str(stone)
    if len(str_stone) % 2 == 1:
        return [stone * 2024]
    mid = len(str_stone) // 2
    return [int(str_stone[:mid]), int(str_stone[mid:])]


def single_stone_blinking(stone: int, num_of_blinks: int) -> int:
    if num_of_blinks == 0:
        return 1
    if num_of_blinks in memory_table[stone]:
        return memory_table[stone][num_of_blinks]
    stones = apply_rules(stone)
    result = sum(single_stone_blinking(s, num_of_blinks - 1) for s in stones)
    memory_table[stone][num_of_blinks] = result
    return result


def blinking(stones: List[int], num_of_blinks: int) -> int:
    return sum(single_stone_blinking(stone, num_of_blinks) for stone in stones)


def part1(stones) -> int:
    return blinking(stones, 25)


def part2(stones) -> int:
    return blinking(stones, 75)


def solve(input):
    with open(input) as file:
        stones = list(map(int, file.read().strip().split()))

    return (part1(stones), part2(stones))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])
