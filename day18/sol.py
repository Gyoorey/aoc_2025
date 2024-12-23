from typing import List, Tuple
import numpy as np


def part1(bytes: List[Tuple[int, int]], max_range = 71) -> int:
    memory = np.zeros((max_range, max_range), dtype=int)
    for x, y in bytes:
        memory[y, x] = -1
    wavefront = [(0, 0)]
    while wavefront:
        x, y = wavefront.pop(0)
        neighbours = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for n in neighbours:
            nx, ny = n
            if nx < 0 or nx >= max_range or ny < 0 or ny >= max_range:
                continue
            if memory[ny, nx] == 0:
                memory[ny, nx] = memory[y, x] + 1
                wavefront.append((nx, ny))
    
    return memory[max_range-1, max_range-1]

def part2(bytes: List[Tuple[int, int]]) -> int:
    left, right = 1024, len(bytes)
    while left < right:
        mid = (left + right) // 2
        if part1(bytes[:mid]) == 0:
            right = mid
        else:
            left = mid + 1
    return bytes[left - 1]

def solve(input):
    with open(input) as file:
        lines = [line.strip() for line in file.readlines()]
        bytes = [(int(line.split(",")[0]), int(line.split(",")[1])) 
                 for line in lines]

    return part1(bytes[:1024], max_range=71), part2(bytes)


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])