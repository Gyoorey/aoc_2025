from typing import Dict, List, Tuple
import numpy as np
import re
from trie import Trie

def part1(messages: List[str], patterns: List[str]) -> int:
    patterns = r"(" + r"|".join(patterns) + r")+$"
    matched = filter(lambda x: re.match(patterns, x), messages)

    return len(list(matched))

memory_map = {}

def decompose(message: str, trie: Trie, path: str, original: str) -> int:
    if message in memory_map:
        return memory_map[message]

    prefix_indices = trie.startsWithAll(message)
    num_of_decomp = 0
    for prefix_index in prefix_indices:
        path_temp = path + message[:prefix_index]
        if path_temp == original:
            num_of_decomp += 1
        else:
            num_of_decomp += decompose(message[prefix_index:], trie, path_temp, original)

    memory_map[message] = num_of_decomp
    return num_of_decomp

def part2(messages: List[str], patterns: List[str]) -> int:      
    # it could be solved with a simple startswith, but let's learn something new
    trie = Trie()
    for pattern in patterns:
        trie.insert(pattern)
    num_of_decomp = sum(decompose(message, trie, '', message) for message in messages)

    return num_of_decomp


def solve(input):
    with open(input) as file:
        lines = [line.strip() for line in file.readlines()]
        patterns: List[str] = lines[0].split(", ")
        messages: List[str] = lines[2:]

    return (part1(messages.copy(), patterns.copy()), 
            part2(messages.copy(), patterns.copy()))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])