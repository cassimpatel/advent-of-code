import re

def parse_input(input):
    cmds = [int(x) if x.isdigit() else x for x in re.findall('(\d+|[A-Za-z]+)', input.split('\n\n')[1])]
    grid = [[y for y in x] for x in input.split('\n\n')[0].split('\n')]

    # padding grid with ' ' to allow for easier boundary checking later
    maxW = max([len(x) for x in grid]) + 2
    grid = [[' '] * maxW] + [[' '] + x + [' '] * (maxW - len(x) - 1) for x in grid] + [[' '] * maxW]

    return grid, cmds

# takes current x, y and proposed direction of movement (into void), returns new x, y, dirIndex on the map
# wraps around map according to rules in part 1
def basic_wrap_around(grid, x, y, dirIndex):
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)] # > v < ^

    # move in the opposite direction until finding the wrap around location
    dx, dy = dirs[(dirIndex + 2) % 4]
    nx, ny = x, y
    while grid[ny + dy][nx + dx] != ' ':
        nx, ny = nx + dx, ny + dy

    return nx, ny, dirIndex

# wraps around map according to rules in part 2 (the map is a cube)
# hardcodes due to all test inputs having the same cube layout (doesn't work on example input)
def cube_wrap_around(grid, x, y, dirIndex):
    # map down by one in each direction to account for padding added
    x, y = x - 1, y - 1
    # calculate face in each direction and offset from its face
    faceX, offsetX = x // 50, x % 50
    faceY, offsetY = y // 50, y % 50

    # maps (faceX, faceY, dirIndex) -> (nx, ny, newDirIndex) according to https://imgur.com/a/K9Of42d
    # we only consider the ways you can enter the void from the map
    cube_wrapping = {
        # face 1: can go >, v or ^
        (2, 0, 0): (99,      99 + (50 - offsetY), 2),
        (2, 0, 1): (99,      50 + (offsetX),      2),
        (2, 0, 3): (offsetX, 199,                 3),

        # face 2: can go < or ^
        (1, 0, 2): (0, 99 + (50 - offsetY), 0),
        (1, 0, 3): (0, 150 + offsetX,       0),

        # face 3: can go > or <
        (1, 1, 0): (100 + offsetY, 49,  3),
        (1, 1, 2): (offsetY,       100, 1),

        # face 4: can go > or v
        (1, 2, 0): (149, 49 - offsetY,  2),
        (1, 2, 1): (49,  150 + offsetX, 2),

        # face 5: can go < or ^
        (0, 2, 2): (50, 49 - offsetY, 0),
        (0, 2, 3): (50, 50 + offsetX, 0),

        # face 6: can go >, v or <
        (0, 3, 0): (50 + offsetY,  149, 3),
        (0, 3, 1): (100 + offsetX, 0,   1),
        (0, 3, 2): (50 + offsetY,  0,   1)
    }

    nx, ny, newDirIndex = cube_wrapping[(faceX, faceY, dirIndex)]
    # map back to grid indices with padding
    return nx + 1, ny + 1, newDirIndex

# takes raw input and function to handle map wrap around
def get_password(input, wrap_around_func):
    grid, cmds = parse_input(input)

    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)] # > v < ^
    x, y = grid[1].index('.'), 1
    dirIndex = 0

    for cmd in cmds:
        if type(cmd) == int:
            for _ in range(cmd):
                dx, dy = dirs[dirIndex]
                nx, ny = x + dx, y + dy
                
                if grid[ny][nx] == ' ':
                    # proposed location is in void: find new loc, dir by wrap around func
                    nx, ny, dirIndex = wrap_around_func(grid, x, y, dirIndex)
                
                if grid[ny][nx] == '#': break
                x, y = nx, ny
        else:
            dirIndex = (dirIndex + 1) % 4 if cmd == 'R' else (dirIndex - 1) % 4
        # print("command: {}, loc: {}, dir: {}".format(cmd, (x-1, y-1), dirs[dir]))
    
    return 1000 * y + 4 * x + dirIndex

def day22_part1(input):
    return get_password(input, basic_wrap_around)

def day22_part2(input):
    return get_password(input, cube_wrap_around)

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day22_part1(example_input) == 6032
    print(day22_part1(test_input))

    # solution is hardcoded to test input size and format: don't run for example
    # assert day22_part2(example_input) == 1
    print(day22_part2(test_input))