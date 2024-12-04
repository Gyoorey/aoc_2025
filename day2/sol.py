
from typing import List


def diff(lst: List[int]) -> List[int]:
    return [lst[i] - lst[i+1] for i in range(len(lst)-1)]


def is_safe(level: List[int]) -> bool:
    return (all(e > 0 for e in level) or
            all(e < 0 for e in level)) and \
        all(1 <= abs(d) <= 3 for d in level)


def solve(input):
    with open(input) as file:
        lines = file.readlines()
        levels = [list(map(int, line.split())) for line in lines]
        safe_count = sum([1 for level in levels if is_safe(diff(level))])

        safe_count2 = sum([1 for level in levels if is_safe(diff(level)) or
                           any(is_safe(diff(list(level[:i] + level[i+1:]))) for i in range(len(level)))])

        return safe_count, safe_count2


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])
