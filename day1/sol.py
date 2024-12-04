
def solve(input):
    with open(input) as file:
        lines = file.readlines()
        pairs = [map(int, line.split()) for line in lines]
        left, right = zip(*pairs)
        left, right = sorted(left), sorted(right)
        distance = [abs(left[i] - right[i]) for i in range(len(left))]

        similarity_score = sum([item * right.count(item) for item in left])

        return sum(distance), similarity_score


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])
