
def solve(input, remove=False):
    with open(input) as file:
        line = file.read()
        sum_ = 0
        if remove:
            while line.find("don't()") != -1:
                dont_index = line.find("don't()")
                do_index = line[dont_index:].find("do()")
                if do_index == -1:
                    line = line[:dont_index]
                else:
                    line = line[:dont_index] + line[dont_index + do_index+4:]
        muls = line.split("mul(")
        params = [param.split(")")[0] for param in muls]
        pairs = [list(map(int, param.split(","))) for param in params if
                 param.count(",") == 1 and
                 param.split(",")[0].isdecimal() and
                 param.split(",")[1].isdecimal() and
                 1 <= len(param.split(",")[0]) <= 3 and
                 1 <= len(param.split(",")[1]) <= 3]
        sum_ += sum([pair[0] * pair[1] for pair in pairs])

    return sum_


if __name__ == "__main__":
    input = "input.txt"
    print("Part 1: ", solve(input))
    print("Part 2: ", solve(input, remove=True))
