import itertools
from operator import add, mul
from typing import List


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def try_to_solve(operands: List[int], result: int, operators: List[callable]) -> int:
    operator_comb = list(itertools.product(operators, repeat=len(operands)-1))
    for combination in operator_comb:
        temp = operands[0]
        for j in range(len(operands)-1):
            temp = combination[j](temp, operands[j+1])
        if temp == result:
            return result
    return 0


def calibration(results: List[int], operands_list: List[List[int]], use_concat: bool = False) -> int:
    sum_ = 0
    operators = [add, mul]
    if use_concat:
        operators.append(concat)
    solutions = [try_to_solve(operands_list[i], results[i], operators[:2])
                 for i in range(len(results))]
    sum_ += sum(solutions)

    if use_concat:
        sum_ += sum(try_to_solve(operands_list[i], results[i], operators)
                    for i in range(len(results)) if solutions[i] == 0)

    return sum_


def part1(results: List[int], operands: List[List[int]]) -> int:
    return calibration(results=results, operands_list=operands)


def part2(results: List[int], operands: List[List[int]]) -> int:
    return calibration(results=results, operands_list=operands, use_concat=True)


def solve(input):
    with open(input) as file:
        lines = file.readlines()
        equations = [list(map(int, line.strip().replace(":", "").split(" ")))
                     for line in lines]
        results = [equation[0] for equation in equations]
        operands = [equation[1:] for equation in equations]

        return part1(results=results, operands=operands), part2(results=results, operands=operands)


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])
