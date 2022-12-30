import re

def parse_input(input):
    cmds = [int(x) if x.isdigit() else x for x in re.findall('(\d+|[A-Za-z]+)', input.split('\n\n')[1])]
    grid = [[y for y in x] for x in input.split('\n\n')[0].split('\n')]

    # padding grid with ' ' to allow for easier boundary checking later
    maxW = max([len(x) for x in grid])
    grid = [[' '] * (maxW + 2)] + [[' '] + x + [' '] * (maxW - len(x) + 1) for x in grid] + [[' '] * (maxW + 2)]

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
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)] # > v < ^
    nx, ny, newDirIndex = 0, 0, 0

    # map down by one in each direction to account for padding added
    x, y = x-1, y-1
    # calculate face in each direction and offset from its face
    faceX, faceY = x // 50, y // 50
    offsetX, offsetY = x % 50, y % 50

    # TODO: a dictionary mapping (faceX, faceY, dirIndex) -> (nx, ny, newDirIndex) to avoid using lengthy ifs

    # looking at each faces 1...6 in https://imgur.com/a/K9Of42d for reference
    # for each of these faces, considering directions from this face to the void
    if (faceX, faceY) == (2, 0):
        # face 1: can go >, v or ^
        if dirIndex == 0:
            nx, ny, newDirIndex = 99, 99 + (50 - offsetY), 2
        elif dirIndex == 1:
            nx, ny, newDirIndex = 99, 50 + (offsetX), 2
        elif dirIndex == 3:
            nx, ny, newDirIndex = offsetX, 199, 3
    elif (faceX, faceY) == (1, 0):
        # face 2: can go < or ^
        if dirIndex == 2:
            nx, ny, newDirIndex = 0, 99 + (50 - offsetY), 0
        elif dirIndex == 3:
            nx, ny, newDirIndex = 0, 150 + offsetX, 0
    elif (faceX, faceY) == (1, 1):
        # face 3: can go > or <
        if dirIndex == 0:
            nx, ny, newDirIndex = 100 + offsetY, 49, 3
        elif dirIndex == 2:
            nx, ny, newDirIndex = offsetY, 100, 1
    elif (faceX, faceY) == (1, 2):
        # face 4: can go > or v
        if dirIndex == 0:
            nx, ny, newDirIndex = 0, 0, 0
        elif dirIndex == 1:
            nx, ny, newDirIndex = 0, 0, 0
    elif (faceX, faceY) == (0, 2):
        # face 5: can go < or ^
        if dirIndex == 2:
            nx, ny, newDirIndex = 0, 0, 0
        elif dirIndex == 3:
            nx, ny, newDirIndex = 0, 0, 0
    elif (faceX, faceY) == (0, 3):
        # face 6: can go >, v or <
        if dirIndex == 0:
            nx, ny, newDirIndex = 0, 0, 0
        elif dirIndex == 1:
            nx, ny, newDirIndex = 0, 0, 0
        elif dirIndex == 2:
            nx, ny, newDirIndex = 0, 0, 0

    # mapping back to grid indices with padding
    nx, ny = nx + 1, ny + 1
    return nx, ny, newDirIndex

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
    # same to previous solution but when running off a side: send x, y and dx, dy to a function
    # function will look at % 50 (or 4 if test input) to determine which face being walked off of
    # can then map back to exact location using offset from original face
    
    return None

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day22_part1(example_input) == 6032
    print(day22_part1(test_input))

    # assert day22_part2(example_input) == 1
    # print(day22_part2(test_input))