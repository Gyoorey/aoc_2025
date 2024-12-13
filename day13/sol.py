
from math import ceil, inf
import re


def claw_machine(As, Bs, prizes) -> int:
    a_cost = 3
    b_cost = 1
    result = 0
    for (ax, ay), (bx, by), (px, py) in zip(As, Bs, prizes):
        tokens = []
        # first solution
        offset = py - px * ay / ax
        x = offset / (by / bx - ay / ax)
        if abs(x - round(x)) < 1e-3:
            num_b = int(round(x)) // bx
            num_a = (px - num_b * bx) // ax
            if num_a*ax + num_b*bx == px and num_a*ay + num_b*by == py:
                tokens.append(a_cost * num_a + b_cost * num_b)
        # second solution
        offset = py - px * by / bx
        x = offset / (ay / ax - by / bx)
        if abs(x - round(x)) < 1e-3:
            num_a = int(round(x)) // ax
            num_b = (px - num_a * ax) // bx
            if num_a*ax + num_b*bx == px and num_a*ay + num_b*by == py:
                tokens.append(a_cost * num_a + b_cost * num_b)
        if tokens:
            result += min(tokens)

    return result


def part1(As, Bs, prizes) -> int:
    return claw_machine(As, Bs, prizes)


def part2(As, Bs, prizes) -> int:
    prizes = [(px + 10000000000000, py + 10000000000000) for px, py in prizes]
    return claw_machine(As, Bs, prizes)


def solve(input):
    button_pattern = r"Button (\w+): X([+-]?\d+), Y([+-]?\d+)"
    prize_pattern = r"Prize: X=(\d+), Y=(\d+)"
    A = []
    B = []
    prize = []
    with open(input) as file:
        lines = [line.strip() for line in file.readlines()]
        for i in range(0, len(lines), 4):
            A_match = re.match(button_pattern, lines[i])
            A.append((int(A_match.group(2)), int(A_match.group(3))))
            B_match = re.match(button_pattern, lines[i + 1])
            B.append((int(B_match.group(2)), int(B_match.group(3))))
            prize_match = re.match(prize_pattern, lines[i + 2])
            prize.append((int(prize_match.group(1)),
                         int(prize_match.group(2))))

    return (part1(A, B, prize), part2(A, B, prize))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])
