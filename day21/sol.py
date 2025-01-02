
from typing import List, Tuple


class KeyPadRobot:
    def __init__(self):
        self.position = self.get_position_of_key('A')

    def get_position_of_key(self, key):
        match key:
            case '1': return (2, 0)
            case '2': return (2, 1)
            case '3': return (2, 2)
            case '4': return (1, 0)
            case '5': return (1, 1)
            case '6': return (1, 2)
            case '7': return (0, 0)
            case '8': return (0, 1)
            case '9': return (0, 2)
            case '0': return (3, 1)
            case 'A': return (3, 2)

    def move_to(self, target_key):
        y, x = self.position
        y_t, x_t = self.get_position_of_key(target_key)
        # order: left, down, up, right
        if y_t <= y:
            if x_t <= x:
                if x_t == 0:
                    ret = '^' * (y - y_t) + '<' * x
                else:    
                    ret = '<' * (x - x_t) + '^' * (y - y_t)
            if x_t > x:
                ret = '^' * (y - y_t) + '>' * (x_t - x)
        if y_t > y:
            if x_t <= x:
                ret = '<' * (x - x_t) + 'v' * (y_t - y)
            if x_t > x:
                ret = 'v' * (y_t - y) + '>' * (x_t - x)

        return ret
    
    def generate_inputs(self, target_key):
        moves = self.move_to(target_key)
        self.position = self.get_position_of_key(target_key)
        return moves + 'A'

class ArrowPadRobot:
    def __init__(self):
        self.position = (0, 2)
        # order: left, down, up, right
        self.moves = {
            ('A', '<'): "v<<",
            ('A', '>'): "v",
            ('A', '^'): "<",
            ('A', 'v'): "<v",
            ('^', '<'): "v<",
            ('^', '>'): "v>",
            ('v', '<'): "<",
            ('v', '>'): ">",
            ('<', '>'): ">>",
            ('<', 'A'): ">>^",
            ('>', 'A'): "^",
            ('^', 'A'): ">",
            ('v', 'A'): "^>",
            ('<', '^'): ">^",
            ('<', 'v'): ">",
            ('>', '^'): "<^",
            ('>', 'v'): "<",
            ('>', '<'): "<<",
            ('^', '^'): "",
            ('v', 'v'): "",
            ('<', '<'): "",
            ('>', '>'): "",
            ('A', 'A'): ""
        }

    def generate_inputs(self, output, prev='A'):
        input = ''
        for o in output:
            input += self.moves[(prev, o)] + 'A'
            prev = o
        
        return input
        
def complexity(code, user_input):
    return len(user_input) * int(code[:-1])

def do_12_rounds(moves: Tuple[str, str], memory):
    robot = ArrowPadRobot()
    pattern = moves
    prev = moves[0]
    moves = moves[1]
    moves = robot.generate_inputs(moves, prev=prev)
    for _ in range(11):
        moves = robot.generate_inputs(moves)
    memory[tuple(pattern)] = moves
        
def part1(codes):
    complexity_sum = 0
    for code in codes:
        robot1 = KeyPadRobot()
        robot2 = ArrowPadRobot()
        moves = ''
        for c in code:
            moves += robot1.generate_inputs(c)
        for _ in range(2):
            moves = robot2.generate_inputs(moves)
        complexity_sum += complexity(code, moves)
    return complexity_sum

# strategy: generate all possible moves for 12 rounds and store them in memory
# then for each code, generate the moves for the first robot, then use the memory 
# to generate the moves for the 25 plus iterations and calculate the complexities
def part2(codes):
    robot = ArrowPadRobot()
    memory = {}
    for key in robot.moves.keys():
        do_12_rounds(key, memory)
    sum_complexity = 0
    for code in codes:
        robot1 = KeyPadRobot()
        moves1 = ''
        for c in code:
            moves1 += robot1.generate_inputs(c)
        # it = 1
        moves1 = robot.generate_inputs(moves1)
        # it = 13
        first = 'A'
        moves13 = ''
        for i in range(len(moves1)):
            second = moves1[i]
            moves13 += memory[(first, second)]
            first = second
        # it = 25 (here only use the length of the moves)
        first = 'A'
        code_len = 0
        for i in range(len(moves13)):
            second = moves13[i]
            code_len += len(memory[(first, second)])
            first = second    
        sum_complexity += code_len * int(code[:-1])
    return sum_complexity
# a more sophisticated approach would be to store move pairs for all depths and
# build a recursive tree with caching


def solve(input):
    with open(input) as file:
        codes = [line.strip() for line in file.readlines()]

    return (part1(codes), part2(codes))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])