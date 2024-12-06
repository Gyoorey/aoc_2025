
from enum import IntEnum
import re
from typing import List, Set, Tuple


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Hit:
    def __init__(self, position: Tuple[int, int], direction: Direction):
        self.position = position
        self.direction = direction

    def __eq__(self, other):
        if isinstance(other, Hit):
            return self.position == other.position and self.direction == other.direction
        return False

    def __hash__(self):
        return hash((self.position, self.direction))


def move(position: Tuple[int, int], direction: Direction) -> Tuple[int, int]:
    match direction:
        case Direction.UP:
            return (position[0]-1, position[1])
        case Direction.RIGHT:
            return (position[0], position[1]+1)
        case Direction.DOWN:
            return (position[0]+1, position[1])
        case Direction.LEFT:
            return (position[0], position[1]-1)


def turn_right(direction: Direction) -> Direction:
    return Direction((direction+1) % len(Direction))


def part1(position: Tuple[int, int],
          direction: Direction,
          lab: List[str]) -> int:
    N, M = len(lab), len(lab[0])
    # keep track of visited positions
    visited_positions: Set[int] = set()
    # keep track of visited obstacles (required for loop detection [part2])
    visited_obstacles: Set[Hit] = set()
    loop_detected = False
    while True:
        visited_positions.add(position[0]*M + position[1])
        next_position = move(position, direction)
        # we left the lab
        if not (0 <= next_position[0] < N and
                0 <= next_position[1] < M):
            break
        # we hit an obstacle
        if lab[next_position[0]][next_position[1]] == "#":
            hit = Hit(next_position, direction)
            # same direction again...
            if hit in visited_obstacles:
                loop_detected = True
                break
            visited_obstacles.add(hit)
            direction = turn_right(direction)
            continue
        position = next_position

    return len(visited_positions), loop_detected


def insert_obstacle(lab: List[str], position: Tuple[int, int]) -> List[str]:
    new_lab = lab.copy()
    new_lab[position[0]] = new_lab[position[0]][:position[1]] + \
        "#" + new_lab[position[0]][position[1]+1:]

    return new_lab


def part2(position: Tuple[int, int],
          direction: Direction,
          lab: List[str]) -> int:
    M = len(lab[0])
    points = re.finditer(r".", "".join(lab))
    test_position = [(match.start()//M, match.start() % M)
                     for match in points]
    exh_search = [part1(position,
                        direction,
                        insert_obstacle(lab, tp))[1]
                  for tp in test_position]

    return exh_search.count(True)


def solve(input):
    with open(input) as file:
        lab = [line.strip() for line in file.readlines()]
        M = len(lab[0])
        init_position = re.search(r"[<>v^]", "".join(lab))
        match init_position.group():
            case "^":
                direction = Direction.UP
            case "v":
                direction = Direction.DOWN
            case "<":
                direction = Direction.LEFT
            case ">":
                direction = Direction.RIGHT
        position = (init_position.start()//M, init_position.start() % M)

    return (part1(position, direction, lab)[0],
            part2(position, direction, lab))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])
