from typing import Dict, List
from functools import cmp_to_key


def part1(rules: Dict[int, List[int]], updates: List[List[int]]) -> int:
    sum_ = sum([update[len(update)//2] for update in updates if
                not any([rules[update[j]].count(update[i]) > 0
                         for i in range(len(update))
                         for j in range(i+1, len(update))])])

    return sum_


def part2(rules: Dict[int, List[int]], original_updates: List[List[int]]) -> int:
    sorted_updates = [sorted(update, key=cmp_to_key(
        lambda x, y: -1 if x in rules and y in rules[x] else 1)) for update in original_updates]

    return part1(rules, sorted_updates) - part1(rules, original_updates)


def solve(input):
    with open(input) as file:
        lines = file.readlines()
        separator_index = lines.index("\n")
        pairs = [list(map(int, line.strip().split("|")))
                 for line in lines[:separator_index]]
        rules = {x: [y for _, y in pairs if _ == x] for x, _ in pairs}
        updates = [list(map(int, line.strip().split(",")))
                   for line in lines[separator_index+1:]]

    return (part1(rules, updates), part2(rules, updates))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])
