
from collections import defaultdict
from typing import List
import numpy as np


class RNG:
    def __init__(self, seed):
        self.seed = seed
    
    def next(self):
        seed = self.seed
        seed = ((seed * 64) ^ seed) % 16777216
        seed = ((seed // 32) ^ seed) % 16777216
        seed = ((seed * 2048) ^ seed) % 16777216
        self.seed = seed
        return self.seed


def part1(seeds):
    prices = []
    sum_ = 0
    for seed in seeds:
        rng = RNG(seed)
        numbers = [seed % 10] + [rng.next() % 10 for _ in range(2000)]
        prices.append(numbers)
        sum_ += rng.seed

    return sum_, prices


def part2(prices: List[List[int]]):
    changes = defaultdict(lambda: defaultdict(int))
    prices = np.array(prices)
    for i, row in enumerate(prices):
        diffs = np.diff(row)
        for j in range(len(diffs) - 3):
            if not i in changes[tuple(diffs[j:j+4])]:
                changes[tuple(diffs[j:j+4])][i] = row[j+4]
    num_of_bananas = max(sum(buyers.values()) for _, buyers in changes.items())

    return num_of_bananas


def solve(input):
    with open(input) as file:
        seeds = [int(line.strip()) for line in file.readlines()]
    part1_result, numbers = part1(seeds)

    return (part1_result, part2(numbers))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])