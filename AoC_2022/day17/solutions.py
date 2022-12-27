# returns new rock location and whether or not it has moved
def move_rock(chamber, rock, dir):
    dirs = {'<':(-1, 0), '>':(1, 0), 'v':(0, -1)}
    dx, dy = dirs[dir]

    x = [x for (x, y) in rock]
    minX, maxX = min(x), max(x)

    newRock = []

    if dir == '<' and minX == 0: return rock, False
    if dir == '>' and maxX == 6: return rock, False

    for (x, y) in rock:
        nx, ny = x + dx, y + dy
        if (nx, ny) in chamber: return rock, False
        newRock.append((nx, ny))

    return newRock, True

def get_chamber_str(chamber, maxHeight):
    result_str = ''

    for y in range(maxHeight, maxHeight - 25, -1):
        if y <= 0: break
        row_vals = ['#' if (x, y) in chamber else '.' for x in range(7)]
        result_str += ''.join(row_vals) + '\n'

    # print(result_str)
    return result_str

def getMaxHeight(jets, num_rocks):
    rocks = [
        [(2, 0), (3, 0), (4, 0), (5, 0)],
        [(2, 1), (3, 0), (3, 1), (3, 2), (4, 1)],
        [(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(2, 0), (2, 1), (3, 0), (3, 1)]
    ]
    chamber = set([(x, 0) for x in range(7)])

    jetIndex, rockIndex = 0, 0
    maxHeight, num_rocks_fallen = 0, 0
    
    # vars for loop checking: we save all states until we see one we've visited before
    num_loops, heightGainPerLoop = 0, 0
    loop_found = False
    states = {}

    while num_rocks_fallen < num_rocks:
        rockIndex = num_rocks_fallen % len(rocks)
        currRock = [(x, y + maxHeight + 4) for (x, y) in rocks[rockIndex]]
        moved = True

        while moved:
            currJet = jets[jetIndex]
            currRock, _ = move_rock(chamber, currRock, currJet)
            currRock, moved = move_rock(chamber, currRock, 'v')

            if not moved:
                chamber.update(currRock)
                maxHeight = max([maxHeight] + [y for (x, y) in currRock])
                num_rocks_fallen += 1
                # print(num_rocks_fallen, maxHeight)

                state = (rockIndex, jetIndex, get_chamber_str(chamber, maxHeight))
                if not loop_found and state in states:
                    (prevMaxHeight, prevNumRocks) = states[state]
                    loop_found = True
                    
                    # calc number of rocks fallen for the loop to occur, and how much higher the chamber is
                    # we can then jump to the last occurrence of the loop and continue from there
                    loopLen = num_rocks_fallen - prevNumRocks
                    heightGainPerLoop = maxHeight - prevMaxHeight
                    num_loops = (num_rocks - num_rocks_fallen) // loopLen
                    num_rocks_fallen += num_loops * loopLen
                else: states[state] = (maxHeight, num_rocks_fallen)

            jetIndex = (jetIndex + 1) % len(jets)

    # add on the height gained during each of the skipped loops
    return maxHeight + heightGainPerLoop * num_loops
    
def day17_part1(input):
    jets = [x for x in input]

    return getMaxHeight(jets, 2022)

def day17_part2(input):
    jets = [x for x in input]
    return getMaxHeight(jets, 1000000000000)

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day17_part1(example_input) == 3068
    print(day17_part1(test_input))

    assert day17_part2(example_input) == 1514285714288
    print(day17_part2(test_input))