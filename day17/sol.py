
import math

cout = []

def decode_combo(operand, A, B, C):
    if operand <= 3:
        return operand
    match operand:
        case 4:
            return A
        case 5:
            return B
        case 6:
            return C
        case 7:
            return 7

def adv(operand, A, B, C, ip):   
    operand = decode_combo(operand, A, B, C)
    return A // (2 **operand), B, C, ip+2

def bxl(operand, A, B, C, ip):
    return A, operand ^ B, C, ip+2

def bst(operand, A, B, C, ip):
    operand = decode_combo(operand, A, B, C)
    return A, operand % 8, C, ip+2

def jnz(operand, A, B, C, ip):
    if A == 0:
        return A, B, C, ip+2
    return A, B, C, operand

def bcx(operand, A, B, C, ip):
    return A, B ^ C, C, ip+2

def out_(operand, A, B, C, ip):
    global cout
    operand = decode_combo(operand, A, B, C)
    cout.append(operand % 8)
    return A, B, C, ip+2

def bdv(operand, A, B, C, ip):
    operand = decode_combo(operand, A, B, C)
    return A, A // (2 **operand), C, ip+2

def cdv(operand, A, B, C, ip):
    operand = decode_combo(operand, A, B, C)
    return A, B, A // (2 **operand), ip+2

opcodes = [adv, bxl, bst, jnz, bcx, out_, bdv, cdv]

def part1(program, A, B, C):
    global cout
    ip = 0
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip+1]
        A, B, C, ip = opcodes[opcode](operand, A, B, C, ip)

    return cout

def part2(program, A, B, C):
    global cout
    solutions = [[0], [1], [2], [3], [4], [5], [6], [7]]
    while True: 
        new_solutions = []
        for sol in solutions:
            for i in range(8):
                cout = []
                temp = sol + [i]
                temp_int = int("".join(map(str, temp)), 8)
                ret = part1(program, temp_int, 0, 0)
                if ret == program[-len(ret):]:
                    new_solutions.append(temp)
        if new_solutions == []:
            break 
        solutions = new_solutions
    int_solutions = [int("".join(map(str, sol)), 8) for sol in solutions]

    return min(int_solutions)

def solve(input):
    with open(input) as file:
        lines = [line.strip() for line in file.readlines()]
        A = int(lines[0].split(" ")[-1])
        B = int(lines[1].split(" ")[-1])
        C = int(lines[2].split(" ")[-1])
        program = list(map(int, lines[4].split(" ")[1].split(",")))
    
    ret = part1(program, A, B, C)
    ret = ",".join(map(str, ret))

    return ret , part2(program, A, B, C)


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])
    

        