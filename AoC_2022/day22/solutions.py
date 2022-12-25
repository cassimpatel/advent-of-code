import re

def day22_part1(input):
    cmds = [int(x) if x.isdigit() else x for x in re.findall('(\d+|[A-Za-z]+)', input.split('\n\n')[1])]
    grid = [[y for y in x] for x in input.split('\n\n')[0].split('\n')]

    # padding grid with ' ' to allow for easier boundary checking later
    maxW = max([len(x) for x in grid])
    grid = [[' '] * (maxW + 2)] + [[' '] + x + [' '] * (maxW - len(x) + 1) for x in grid] + [[' '] * (maxW + 2)]

    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)] # > v < ^
    
    x, y = grid[1].index('.'), 1
    dir = 0

    for cmd in cmds:
        if type(cmd) == int:
            for _ in range(cmd):
                dx, dy = dirs[dir]
                nx, ny = x + dx, y + dy
                
                if grid[ny][nx] == ' ':
                    # move in opposite dir until you find wrap around loc
                    dx, dy = dirs[(dir + 2) % 4]
                    nx, ny = x, y
                    while grid[ny + dy][nx + dx] != ' ':
                        nx, ny = nx + dx, ny + dy
                
                if grid[ny][nx] == '#': break
                x, y = nx, ny
        else:
            dir = (dir + 1) % 4 if cmd == 'R' else (dir - 1) % 4
        # print("command: {}, loc: {}, dir: {}".format(cmd, (x-1, y-1), dirs[dir]))
    return 1000 * y + 4 * x + dir

def day22_part2(input):
    # same to previous solution but when running off a side: send x, y and dx, dy to a function
    # function will look at % 50 (or 4 if test input) to determine which face being walked off of
    # then can hardcode maybe using dict what the resulting face to appear on is and with what direction
    # can then map back to exact location using offset from original face
    # use https://imgur.com/a/K9Of42d for reference
    return None

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day22_part1(example_input) == 6032
    print(day22_part1(test_input))

    # assert day22_part2(example_input) == 1
    # print(day22_part2(test_input))