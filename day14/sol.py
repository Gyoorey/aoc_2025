import re
import numpy as np
import matplotlib.pyplot as plt


def move_robots(robots, velocities, max_x, max_y, sim_steps):
    result = [[0 for x in range(max_x)] for y in range(max_y)]
    for i in range(len(robots)):
        robots[i] = [robots[i][0] + velocities[i][0] * sim_steps, 
                     robots[i][1] + velocities[i][1] * sim_steps]
        robots[i] = [robots[i][0] % max_x, robots[i][1] % max_y]
        result[robots[i][1]][robots[i][0]] += 1  

    total_count = 1
    for x_start in [0, max_x//2+1]:
        for y_start in [0, max_y//2+1]:
            count = sum(result[y][x] for y in range(y_start, y_start + max_y//2) 
                        for x in range(x_start, x_start + max_x//2))
            total_count *= count


    return total_count

def has_big_area(result_map,  threshold=10):
    def longest_run_in_row(row):
        max_run = 0
        current_run = 0
        for cell in row:
            if cell > 0:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        return max_run

    threshold = 10
    for row in result_map:
        if longest_run_in_row(row) > threshold:
            return True
    return False


def easter_egg(robots, velocities, max_x, max_y, max_steps):
    robots = np.array(robots)
    velocities = np.array(velocities)
    for sim_steps in range(0, max_steps):
        robot_map = np.zeros((max_y, max_x))
        for robot in robots:
            robot_map[robot[1], robot[0]] = 1
        if has_big_area(robot_map):
            plt.imshow(robot_map)
            plt.savefig(f"{sim_steps}.png")
            plt.close()
            print("Found at", sim_steps)
        robots = (robots + velocities) % [max_x, max_y]

    return 0

def part1(robots, velocities):
    return move_robots(robots, velocities, 101, 103, 100)

def part2(robots, velocities):
    easter_egg(robots, velocities, 101, 103, 10000)
    
    return 0

def solve(input):
    with open(input) as file:
        lines = [line.strip() for line in file.readlines()]
        robots = []
        velocities = []
        for line in lines:
            pattern = r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)"
            m = re.match(pattern, line)
            if m:
                robots.append([int(m.group(1)), int(m.group(2))])
                velocities.append([int(m.group(3)), int(m.group(4))])

    return (part1(robots.copy(), velocities), 
            part2(robots.copy(), velocities))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])